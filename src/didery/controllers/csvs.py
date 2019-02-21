import falcon

from ..help import csving
from ..db import dbing


class CSV:
    def __init__(self, store=None):
        """
        :param store: Store
            store is reference to ioflo data store
        """
        self.store = store

    def on_get(self, req, resp):
        """
        Handle and respond to incoming GET request.

        :param req: Request object
        :param resp: Response object
        """
        resp.status = falcon.HTTP_200
        # resp.content_type = 'text/csv'
        resp.set_header("Content-Disposition", "attachment; filename=\"Responses.csv\"")

        data = dbing.surveyDB.getAll(0, dbing.surveyDB.count())
        data = list(data["data"].values())
        resp.body = csving.to_csv(data).getvalue()
