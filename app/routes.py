import logging
import json

import flask
from flask import Response

import requests
from pprint import pprint

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/combined-stats/<org>", methods=["GET"])
def combined_single(org):
    """
    Simple script if both org names are the same across both platforms
    """
    return combined_double(org, org)


@app.route("/combined-stats/bitbucket/<bitbucket_org>/github/<github_org>", methods=["GET"])
def combined_double_reverse(bitbucket_org, github_org):
    """
    Support both github -> bitbucket and bitbucket -> github ordering
    """
    return combined_double(github_org, bitbucket_org)


@app.route("/combined-stats/github/<github_org>/bitbucket/<bitbucket_org>", methods=["GET"])
def combined_double(github_org, bitbucket_org):
    """
    Gets the combined stats from bitbucket and github
    """
    try:
        # each function throws an exception if the status is something other than 200
        g_resp = github(github_org)
        g = g_resp.json()

        b_resp = bitbucket(bitbucket_org)
        b = b_resp.json()

        resp = {
            "repos": {
                "total": 0,
                "original": 0,
                "forked": 0,
                "unknown_origin": 0
            },
            "watchers": 0,
            "languages": [],
            "topics": []
        }

        for i in g:
            resp["repos"]["total"] += 1
            if i["fork"]:
                resp["repos"]["forked"] += 1
            else:
                resp["repos"]["original"] += 1
            resp["watchers"] += i["watchers"]
            if i["language"] and i["language"].lower() not in resp["languages"]:
                resp["languages"].append(i["language"].lower())
            for t in github_topics(github_org, i["name"]):
                if t.lower() not in resp["topics"]:
                    resp["topics"].append(t)

        for i in b["values"]:
            resp["repos"]["total"] += 1
            # bitbucket doesn't seem to have a way to tell if a repo is a fork or not
            resp["repos"]["unknown_origin"] += 1
            resp["watchers"] += bitbucket_watchers(
                i["links"]["watchers"]["href"])
            if i["language"] and i["language"].lower() not in resp["languages"]:
                resp["languages"].append(i["language"].lower())
            # bitbucket doesn't seem to have topics
    except Exception as err:
        return Response(err, status=500)

    return Response(json.dumps(resp), status=200)


def github(org):
    """
    Gets the github statistics
    """
    resp = requests.get('https://api.github.com/orgs/' + org + '/repos')
    if resp.status_code != 200:
        raise Exception("Github status code: " + str(resp.status_code))
    return resp


def bitbucket(org):
    """
    Gets the bitbucket statistics
    """
    resp = requests.get('https://api.bitbucket.org/2.0/repositories/' + org)
    if resp.status_code != 200:
        raise Exception("Bitbucket status code: " + str(resp.status_code))
    return resp


def bitbucket_watchers(url):
    """
    Gets the watcher count for bitbucket
    """
    # I'm not sure that I like just accepting the url as passed in here
    # I might consider hard coding the url pattern instead, but what if the url pattern changes and the base api doesn't?
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Bitbucket status code: " + str(resp.status_code))
    j = resp.json()
    return j["size"]


def github_topics(org, repo):
    """
    Gets the topics for a repo
    """
    s = requests.session()
    # github has an accept header to get topics as it's a preview feature
    s.headers.update({"accept": "application/vnd.github.mercy-preview+json"})
    resp = s.get('https://api.github.com/repos/' +
                 org + '/' + repo + '/topics')
    if resp.status_code != 200:
        raise Exception("Github status code: " + str(resp.status_code))
    j = resp.json()
    return j["names"]
