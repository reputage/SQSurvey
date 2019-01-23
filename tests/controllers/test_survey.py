try:
    import simplejson as json
except ImportError:
    import json

from didery.routing import *


def testSurvey(client):
    surveyResult = {
        "ip_address": "192.168.1.1"
    }

    response = client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())

    assert json.loads(response.content) == surveyResult

    client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())
    client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())
    client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())

    response = client.simulate_get(SURVEY_BASE_PATH)

    assert len(json.loads(response.content)) == 4

    for survey in json.loads(response.content).values():
        assert survey == surveyResult
