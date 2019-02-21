Background
==========
The project is built on the open source [ioflo](https://github.com/ioflo) framework and also utilizes [click](http://click.pocoo.org/5/), and [lmdb](https://lmdb.readthedocs.io/en/release/) on the back end.

System Requirements
===================
python 3.6  
Linux or macOS  

Development Dependencies
========================
git  
npm  
wheel  

Installation
============

This project depends on [python 3.6](https://www.python.org/downloads/).  You will need to install it if you haven't already.

Clone or download the source from the [SQSurvey Github repo](https://github.com/reputage/SQSurvey) and install from source with:
```
$ pip3 install -e /path/to/sqsurvey
```

Starting The Server
==================
To start up the server simply run the command below

```
$ sqsurvey
```
After running the command a WSGI compatible [Valet](https://github.com/ioflo/ioflo/blob/master/ioflo/aio/http/serving.py) server will have been spun up to listen for web requests.  The default port that sqsurvey will listen on is 8080.

The cli interface for sqsurvey has a couple options that you can see below.

```
Usage: sqsurvey [OPTIONS]

Options:
  -p, --port INTEGER RANGE        Port number the server should listen on.
                                  Default is 8080.
  -V, --version                   Return version.
  -v, --verbose [mute|terse|concise|verbose|profuse]
                                  Verbosity level.
  --path DIRECTORY                Path to the database folder. Defaults to
                                  /var/didery/db.
  --help                          Show this message and exit.

```

The CLI uses click to build its interface.  Unfortunately it doesn't always work well with other tools like circus because of character encodings. For this reason there is an alternative entry point into sqsurvey that uses parseArgs for the cli.  If you run into character encoding errors you can try running sqsurvey as shown below.
```
$ sqsurveyd
```

Testing
=======
You will first need to clone the GitHub repo if you installed using the Pypi wheel. There is one set of unit tests included in the project and can be run using the command:
```
$ pytest --ignore=src/didery/static/
```

Running these tests prior to hosting the server helps ensure that everything in your copy of sqsurvey is working properly.


API
===
The server has two endpoints.
```
http://localhost:8080/surveys
http://localhost:8080/csv
```
/suveys
-------

GET One
-------
Returns the original data uploaded with an ip_address field added
```
http://localhost:8080/surveys/{uuid}
```
Response
```json
{
  "ip_address": "127.0.0.1",
  "survey_data": ""
}
```

GET All
-------
Returns all responses starting at offset up to limit
```
http://localhost:8080/surveys?offset=0&limit=10
```
Response
```json
{
   "data": {
      "uuid": {
          "ip_address": "127.0.0.1",
          "survey_data": ""
      },
      "uuid2": {
          "ip_address": "127.0.0.1",
          "survey_data": ""
      },
      "uuid3": {
          "ip_address": "127.0.0.1",
          "survey_data": ""
      },
      "uuid4": {
          "ip_address": "127.0.0.1",
          "survey_data": ""
      }
   }
}
```


POST
----
Expects a json request body
```
http://localhost:8080/surveys
```

/csv
----

GET
---
will return a .csv file download
```
http://localhost:8080/csv
```
