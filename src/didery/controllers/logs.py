import falcon
import uuid

try:
    import simplejson as json
except ImportError:
    import json

from ..db import dbing


class Logs:
    def __init__(self, store=None):
        """
        :param store: Store
            store is reference to ioflo data store
        """
        self.store = store

    def on_get(self, req, resp, id=None):
        """
            Handle and respond to incoming GET request.
            :param req: Request object
            :param resp: Response object
            :param id: string
                URL parameter specifying a specific log entry
        """
        count = dbing.logDB.count()

        if id is None:
            resp.append_header('X-Total-Count', count)
            body = dbing.logDB.getAll(limit=count)
        else:
            body = dbing.logDB.get(id)
            if body is None:
                raise falcon.HTTPError(falcon.HTTP_404)

        resp.body = json.dumps(body, ensure_ascii=False)
