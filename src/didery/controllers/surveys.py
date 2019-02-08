import falcon
import uuid

try:
    import simplejson as json
except ImportError:
    import json

from ..help import helping
from ..db import dbing


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

    if val < 0:
        raise falcon.HTTPError(falcon.HTTP_400,
                               'Malformed Query String',
                               'url query string value must be a positive number.')

    return key, val


class Survey:
    def __init__(self, store=None):
        """
        :param store: Store
            store is reference to ioflo data store
        """
        self.store = store

    @falcon.before(parseQString)
    def on_get(self, req, resp, id=None):
        """
        Handle and respond to incoming GET request.
        :param req: Request object
        :param resp: Response object
        :param id: string
            URL parameter specifying a specific response
        """
        offset = req.offset
        limit = req.limit

        count = dbing.surveyDB.count()

        if id is None:
            if offset >= count:
                resp.body = json.dumps({"data": {}}, ensure_ascii=False)
                return

            resp.append_header('X-Total-Count', count)
            body = dbing.surveyDB.getAll(offset, limit)
        else:
            body = dbing.surveyDB.get(id)
            if body is None:
                raise falcon.HTTPError(falcon.HTTP_404)

        resp.body = json.dumps(body, ensure_ascii=False)

    def on_post(self, req, resp):
        """
        Handle and respond to incoming POST request.
        :param req: Request object
        :param resp: Response object
        """
        helping.parseReqBody(req)
        body = req.body

        # documentation says remote_addr is a string,
        # but in some cases it's a tuple.
        key = req.remote_addr

        if type(key) is tuple:
            key = key[0]

        # We don't want to lose survey data, so if an ip address
        # cannot be found fall back to uuid's to save the data.
        if type(key) is not str:
            key = str(uuid.uuid4())
            log_data = {
                "title": "Unknown IP Address Format",
                "description": "Could not access requester's IP Address. {}".format(req.remote_addr),
                "request_body": body,
                "remote_addr": req.remote_addr,
                "key": key
            }
            dbing.logDB.save(key, log_data)

        if dbing.surveyDB.get(key) is not None:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   "Resource Already Exists",
                                   "Only one survey response per ip address allowed.")

        dbing.surveyDB.save(key, body)

        resp.body = json.dumps(body, ensure_ascii=False)
        resp.status = falcon.HTTP_201
