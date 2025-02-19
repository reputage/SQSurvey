import falcon
import uuid
import arrow

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
        survey_data = req.body

        # documentation says remote_addr is a string,
        # but in some cases it's a tuple.
        ip_address = req.remote_addr
        key = str(uuid.uuid4())

        if type(ip_address) is tuple:
            ip_address = ip_address[0]

        body = {
            "survey_data": survey_data,
            "metadata": {
                "ip_address": ip_address,
                "received": str(arrow.utcnow())
            }
        }

        # We don't want to lose survey data, so if an ip address
        # cannot be found log it and save the data.
        if type(ip_address) is not str:
            log_data = {
                "title": "Unknown IP Address Format",
                "description": "Could not access requester's IP Address. {}".format(req.remote_addr),
                "request_body": body,
                "remote_addr": req.remote_addr,
                "ip_address": ip_address
            }
            dbing.logDB.save(key, log_data)

        dbing.surveyDB.save(key, body)

        resp.body = json.dumps({key: body}, ensure_ascii=False)
        resp.status = falcon.HTTP_201
