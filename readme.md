Background
==========
The project is built on the open source [ioflo](https://github.com/ioflo) framework and also utilizes [click](http://click.pocoo.org/5/), and [lmdb](https://lmdb.readthedocs.io/en/release/) on the back end.  The frontend is built with [Transcrypt](https://www.transcrypt.org/documentation) and [mithril.js](https://mithril.js.org/).

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

Clone or download the source from the [didery Github repo](https://github.com/reputage/didery.git) and install from source with:
```
$ pip3 install -e /path/to/sqsurvey
```

Starting The Server
==================
To start up the server simply run the command below

```
$ sqsurvey
```
After running the command a WSGI compatible [Valet](https://github.com/ioflo/ioflo/blob/master/ioflo/aio/http/serving.py) server will have been spun up to listen for web requests.  The default port that didery will listen on is 8080.

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

The CLI uses click to build its interface.  Unfortunately it doesn't always work well with other tools like circus because of character encodings. For this reason there is an alternative entry point into didery that uses parseArgs for the cli.  If you run into character encoding errors you can try running didery as shown below.
```
$ sqsurveyd
```

Testing
=======
You will first need to clone the GitHub repo if you installed using the Pypi wheel. There are two sets of unit tests included in the project. The first of which tests the didery backend and can be run using the command:
```
$ pytest --ignore=src/didery/static/
```
The second tests the didery frontend and can be run using these commands:
```
$ cd /path/to/didery/src/didery/static/
$ npm run-script prep-tests
$ npm test
```
Running these tests prior to hosting the server helps ensure that everything in your copy of didery is working properly.


API
===
The server has a single endpoint that will service GET and POST requests
```
http://localhost:8080/surveys
```

* GET will return all entries

* POST expects a json request body