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

```
curl -i "http://127.0.0.1:5000/health-check"
```

```
curl -i "http://127.0.0.1:5000/combined-stats/<org>"
```

```
curl -i "http://127.0.0.1:5000/combined-stats/<org>"
```

```
curl -i "http://127.0.0.1:5000/combined-stats/bitbucket/<bitbucket_org>/github/<github_org>"
curl -i "http://127.0.0.1:5000/combined-stats/github/<github_org>/bitbucket/<bitbucket_org>"
```

## What'd I'd like to improve on...

- A better way of handling the differing organization names for bitbucket and github. Maybe using a different verb?
- Better error handling - build a custom error page that displays detailed error information in addition to a status code
- Instead of using a generic object for the combined profile, make an actual class
- Make a class for github and bitbucket, that both inherit from a base class
