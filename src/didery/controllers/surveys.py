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

        if id is None:
            resp.append_header('X-Total-Count', count)
            body = self.data
        else:
            body = self.data[id]
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

        key = req.remote_addr
        
        if key in self.data:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   "Resource Already Exists",
                                   "Only one survey response per ip address allowed.")

        self.data[key] = body

        resp.body = json.dumps(body, ensure_ascii=False)
        resp.status = falcon.HTTP_201
