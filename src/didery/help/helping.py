import falcon
import tempfile
import os
import shutil

try:
    import simplejson as json
except ImportError:
    import json


def parseReqBody(req):
    """
    :param req: Falcon Request object
    """
    try:
        raw_json = req.stream.read()
    except Exception as ex:
        raise falcon.HTTPError(falcon.HTTP_400,
                               'Request Error',
                               'Error reading request body.')

    try:
        result_json = json.loads(raw_json, encoding='utf-8')
    except ValueError:
        raise falcon.HTTPError(falcon.HTTP_400,
                               'Malformed JSON',
                               'Could not decode the request body. The '
                               'JSON was incorrect.')

    req.body = result_json
    return raw_json


def validateRequiredFields(required, resource):
    """
    Validate that all required fields are present in resource
    :param required: list of required fields
    :param resource: dict to be checked
    """
    for req in required:
        if req not in resource:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Missing Required Field',
                                   'Request must contain {} field.'.format(req))


def parseQString(req, resp, resource, params):
    req.offset = 0
    req.limit = 10

    if req.query_string:
        queries = req.query_string.split('&')
        for query in queries:
            key, val = qStringValidation(query)
            if key == 'offset':
                req.offset = val
            if key == 'limit':
                req.limit = val


def qStringValidation(query):
    keyval = query.split('=')

    if len(keyval) != 2:
        raise falcon.HTTPError(falcon.HTTP_400,
                               'Malformed Query String',
                               'url query string missing value(s).')

    key = keyval[0]
    val = keyval[1]

    try:
        val = int(val)
    except ValueError as ex:
        raise falcon.HTTPError(falcon.HTTP_400,
                               'Malformed Query String',
                               'url query string value must be a number.')

    return key, val


def setupTmpBaseDir():
    """
    Create temporary directory
    """
    return tempfile.mkdtemp(prefix="didery",  suffix="test", dir="/tmp")


def cleanupTmpBaseDir(baseDirPath):
    """
    Remove temporary root of baseDirPath
    Ascend tree to find temporary root directory
    """
    if os.path.exists(baseDirPath):
        shutil.rmtree(baseDirPath)
