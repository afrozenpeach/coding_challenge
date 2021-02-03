# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Install:

You can use a virtual environment (conda, venv, etc):

```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file

```
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run
```

### Making Requests

Check the health of the api server:

```
curl -i "http://127.0.0.1:5000/health-check"
```

Get the combined stats from github and bitbucket when the organization name is the same:

```
curl -i "http://127.0.0.1:5000/combined-stats/<org>"
```

Get the combined stats from github and bitbucket when the organization names are different:

```
curl -i "http://127.0.0.1:5000/combined-stats/bitbucket/<bitbucket_org>/github/<github_org>"
curl -i "http://127.0.0.1:5000/combined-stats/github/<github_org>/bitbucket/<bitbucket_org>"
```

## What'd I'd like to improve on...

- A better way of handling the differing organization names for bitbucket and github. Maybe using a different verb?
- Better error handling - build a custom error page that displays detailed error information in addition to a status code
- Instead of using a generic object for the combined profile, make an actual class
- Make a class for github and bitbucket, that both inherit from a base class
- Unit testing!
  - test the health check route returns All Good and a status 200
  - test each of the 3 github/bitbucket api functions using a dummy org with a set number of repos (alternatively: mock a repo to return)
  - test each of the 3 github/bitbucket api functions on known 404 producing repos (alternatively: mock a 404 result)
  - test the combined_double function for an expected result
