from didery.help.csving import flatten, to_csv
import time


def test_flatten_array():
    dictionary = [{
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
    }]

    headers, values = flatten(dictionary)

    assert headers == ['name', 'street', 'city', 'state', 'zip', 'name', 'street', 'city', 'state', 'zip', 'degree',
                       'favorite_food', 'test_scores', 'test_scores', 'test_scores', 'test_scores', 'image', 'image',
                       'image', 'image', 'image', 'image', 'image', 'image', 'image', 'name', 'age', 'relation', 'name',
                       'age', 'relation']
    assert values == ['Fred Astaire', '546 N 798 W', 'Austin', 'TX', 84057, 'UVU', '546 N 798 W', 'Austin', 'TX', 84057,
                      'Computer Science', 'Pizza', 10, 9, 10, 7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'Frank Astaire', 67,
                      'Father', 'Wilma Astaire', 62, 'Mother']


def test_flatten_dict():
    dictionary = {
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

    headers, values = flatten(dictionary)

    assert headers == ['name', 'street', 'city', 'state', 'zip', 'name', 'street', 'city', 'state', 'zip', 'degree',
                       'favorite_food', 'test_scores', 'test_scores', 'test_scores', 'test_scores', 'image', 'image',
                       'image', 'image', 'image', 'image', 'image', 'image', 'image', 'name', 'age', 'relation', 'name',
                       'age', 'relation']
    assert values == ['Fred Astaire', '546 N 798 W', 'Austin', 'TX', 84057, 'UVU', '546 N 798 W', 'Austin', 'TX', 84057,
                      'Computer Science', 'Pizza', 10, 9, 10, 7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'Frank Astaire', 67,
                      'Father', 'Wilma Astaire', 62, 'Mother']


def test_flatten_empty_array():
    dictionary = []

    headers, values = flatten(dictionary)

    assert headers == []
    assert values == []


def test_flatten_empty_dict():
    dictionary = {}

    headers, values = flatten(dictionary)

    assert headers == []
    assert values == []


def test_speed():
    dictionary = [{
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
    }]
    data = dictionary * 10000
    assert len(data) == 10000

    start = time.process_time()

    for value in data:
        headers, values = flatten(value)

    elapsed = time.process_time() - start
    print(elapsed)


def test_to_csv():
    dictionaries = [{
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
    }] * 10

    exp_data = "name,street,city,state,zip,name,street,city,state,zip,degree,favorite_food,test_scores,test_scores,test_scores,test_scores,image,image,image,image,image,image,image,image,image,name,age,relation,name,age,relation\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n" \
               "Fred Astaire,546 N 798 W,Austin,TX,84057,UVU,546 N 798 W,Austin,TX,84057,Computer Science,Pizza,10,9,10,7,1,2,3,4,5,6,7,8,9,Frank Astaire,67,Father,Wilma Astaire,62,Mother\r\n"

    file = to_csv(dictionaries)
    csv_data = file.getvalue()
    assert csv_data == exp_data
