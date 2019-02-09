import falcon
import uuid

try:
    import simplejson as json
except ImportError:
    import json

from didery.routing import *
from didery.db.dbing import BaseSurveyDB, DB, DB_SURVEY_RESULTS_NAME


def testSurveyPost(client):
    surveyResult = {
        "ip_address": "192.168.1.1"
    }

    response = client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())

    resp_data = json.loads(response.content)
    resp_key = list(resp_data.keys())[0]

    assert len(resp_data) == 1
    assert resp_data[resp_key] == surveyResult


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

    response = client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())

    id = list(json.loads(response.content).keys())[0]

    response = client.simulate_get("{}/{}".format(SURVEY_BASE_PATH, id))

    assert json.loads(response.content) == surveyResult


def testSurveyGetAllInvalidQueryString(client):
    # Test that query params have values
    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset&limit=10")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string missing value(s)."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=10&limit")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string missing value(s)."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result


def testSurveyGetAllInvalidQueryValue(client):
    # Test that query params values are ints
    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=a&limit=10")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string value must be a number."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=10&limit=d")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string value must be a number."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result


def testSurveyGetAllNegativeQueryValue(client):
    # Test that query params values are ints
    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=-1&limit=10")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string value must be a positive number."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=0&limit=-10")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string value must be a positive number."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result


def testSurveyGetAllEmptyQueryValue(client):
    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=10&limit=")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string value must be a number."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=&limit=10")

    exp_result = {
        "title": "Malformed Query String",
        "description": "url query string value must be a number."
    }

    assert response.status == falcon.HTTP_400
    assert json.loads(response.content) == exp_result


def testValidGetAllWithQueryString(client):
    db = BaseSurveyDB(DB(DB_SURVEY_RESULTS_NAME))
    exp_result = {"data": {}}

    for i in range(0, 11):
        history1 = {
            "id": "did:dad:NOf6ZghvGNbFc_wr3CC0tKZHz1qWAR4lD5aM-i0zSjw=",
            "changed": "2000-01-01T00:00:01+00:00",
            "signer": 1,
            "signers": [
                "NOf6ZghvGNbFc_wr3CC0tKZHz1qWAR4lD5aM-i0zSjw=",
                "NOf6ZghvGNbFc_wr3CC0tKZHz1qWAR4lD5aM-i0zSjw=",
                "NOf6ZghvGNbFc_wr3CC0tKZHz1qWAR4lD5aM-i0zSjw="
            ]
        }

        uid = str(uuid.uuid4())
        db.save(uid, history1)
        exp_result["data"][uid] = history1

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=0&limit=11")
    result = json.loads(response.content)

    assert response.status == falcon.HTTP_200
    assert result == exp_result

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=0&limit=20")
    result = json.loads(response.content)

    assert response.status == falcon.HTTP_200
    assert result == exp_result

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=0&limit=0")
    result = json.loads(response.content)

    exp_result = {"data": {}}

    assert response.status == falcon.HTTP_200
    assert result == exp_result

    response = client.simulate_get(SURVEY_BASE_PATH, query_string="offset=100&limit=10")

    assert response.status == falcon.HTTP_200
    assert json.loads(response.content) == exp_result
