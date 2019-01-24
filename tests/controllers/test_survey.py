try:
    import simplejson as json
except ImportError:
    import json

from didery.routing import *


def testSurveyPost(client):
    surveyResult = {
        "ip_address": "192.168.1.1"
    }

    response = client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())

    assert json.loads(response.content) == surveyResult


def testSurveyGetAll(client):
    surveyResult = {
        "ip_address": "192.168.1.1"
    }

    client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())

    response = json.loads(client.simulate_get(SURVEY_BASE_PATH).content)

    assert len(response["data"]) == 1

    for survey in response["data"].values():
        assert survey == surveyResult


def testSurveyGet(client):
    surveyResult = {
        "ip_address": "192.168.1.1"
    }

    client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())

    response = client.simulate_get("{}/{}".format(SURVEY_BASE_PATH, "127.0.0.1"))

    assert json.loads(response.content) == surveyResult
