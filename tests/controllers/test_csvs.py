import falcon

try:
    import simplejson as json
except ImportError:
    import json

from didery.routing import *


def test_csvs_get(client):
    surveyResult = {
        "name": "Fred Astaire",
        "address": {
            "street": "546 N 798 W",
            "city": "Austin",
            "state": "TX",
            "zip": 84057
        },
        "details": {
            "education": {
                "college": {
                    "name": "UVU",
                    "address": {
                        "street": "546 N 798 W",
                        "city": "Austin",
                        "state": "TX",
                        "zip": 84057
                    },
                    "degree": "Computer Science"
                }
            },
            "favorite_food": "Pizza",
            "test_scores": [
                10,
                9,
                10,
                7
            ]
        },
        "image": [
            [1, 2, 3, 4],
            [5, 6, 7],
            [8, 9],
            [],
        ],
        "family": [
            {
                "name": "Frank Astaire",
                "age": 67,
                "relation": "Father"
            },
            {
                "name": "Wilma Astaire",
                "age": 62,
                "relation": "Mother"
            }
        ]
    }

    for i in range(0, 10):
        response = client.simulate_post(SURVEY_BASE_PATH, body=json.dumps(surveyResult).encode())
        assert response.status == falcon.HTTP_201

    response = client.simulate_get(CSVS_BASE_PATH)

    exp_response_headers = b'name,street,city,state,zip,name,street,city,state,zip,degree,favorite_food,test_scores,test_scores,test_scores,test_scores,image,image,image,image,image,image,image,image,image,name,age,relation,name,age,relation,ip_address,received'
    exp_response_value = b'Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother,127.0.0.1'

    response_values = response.content.strip().split(b'\r\n')

    assert response.status == falcon.HTTP_200
    assert response_values[0] == exp_response_headers

    for value in response_values[1:]:
        assert exp_response_value in value
