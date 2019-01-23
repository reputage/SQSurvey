import falcon
import uuid

try:
    import simplejson as json
except ImportError:
    import json

from ..help import helping


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
        count = len(self.data)

        resp.append_header('X-Total-Count', count)

        resp.body = json.dumps(self.data, ensure_ascii=False)

    def on_post(self, req, resp):
        """
        Handle and respond to incoming POST request.
        :param req: Request object
        :param resp: Response object
        """
        helping.parseReqBody(req)
        body = req.body

        key = str(uuid.uuid4())
        self.data[key] = body

        resp.body = json.dumps(body, ensure_ascii=False)
        resp.status = falcon.HTTP_201
