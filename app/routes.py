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
    return combined_double(org, org)


@app.route("/combined-stats/bitbucket/<bitbucket_org>/github/<github_org>", methods=["GET"])
def combined_double_reverse(bitbucket_org, github_org):
    return combined_double(github_org, bitbucket_org)


@app.route("/combined-stats/github/<github_org>/bitbucket/<bitbucket_org>", methods=["GET"])
def combined_double(github_org, bitbucket_org):
    """
    Gets the combined stats from bitbucket and github
    """
    try:
        g_resp = github(github_org)
        g = g_resp.json()

        b_resp = bitbucket(bitbucket_org)
        b = b_resp.json()
    except Exception as err:
        return Response(err, status=500)

    resp = {
        "repos": {
            "total": 0,
            "original": 0,
            "forked": 0,
            "unknown_origin": 0
        },
        "watchers": 0,
        "languages": []
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

    for i in b["values"]:
        resp["repos"]["total"] += 1
        resp["repos"]["unknown_origin"] += 1
        resp["watchers"] += bitbucket_watchers(i["links"]["watchers"]["href"])
        if i["language"] and i["language"].lower() not in resp["languages"]:
            resp["languages"].append(i["language"].lower())

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
    gets the bitbucket statistics
    """
    resp = requests.get('https://api.bitbucket.org/2.0/repositories/' + org)
    if resp.status_code != 200:
        raise Exception("Bitbucket status code: " + str(resp.status_code))
    return resp


def bitbucket_watchers(url):
    """
    gets the watcher count for bitbucket
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Bitbucket status code: " + str(resp.status_code))
    j = resp.json()
    return j["size"]
