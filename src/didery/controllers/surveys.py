import falcon
import uuid

try:
    import simplejson as json
except ImportError:
    import json

from ..help import helping
from ..db import dbing


class Survey:
    def __init__(self, store=None):
        """
        :param store: Store
            store is reference to ioflo data store
        """
        self.store = store
        self.data = {}

    def on_get(self, req, resp, id=None):
        """
        Handle and respond to incoming GET request.
        :param req: Request object
        :param resp: Response object
        :param id: string
            URL parameter specifying a specific response
        """
        count = dbing.surveyDB.count()

        if id is None:
            resp.append_header('X-Total-Count', count)
            body = dbing.surveyDB.getAll(limit=count)
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

        # documentation says remote_addr is a string, but in some cases it is a tuple
        key = req.remote_addr
        if type(key) is tuple:
            key = key[0]
        if type(key) is not str:
            falcon.HTTPError(falcon.HTTP_500,
                             "Unrecoverable Error",
                             "Could not access requestors IP Address. {}".format(req.remote_addr))

        if dbing.surveyDB.get(key) is not None:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   "Resource Already Exists",
                                   "Only one survey response per ip address allowed.")

        dbing.surveyDB.save(key, body)

        resp.body = json.dumps(body, ensure_ascii=False)
        resp.status = falcon.HTTP_201
