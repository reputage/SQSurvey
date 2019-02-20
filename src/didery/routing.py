from didery.controllers import surveys, logs, csvs
SURVEY_BASE_PATH = "/surveys"
LOGS_BASE_PATH = "/logs"
CSVS_BASE_PATH = "/csv"


class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Max-Age:', '3600')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods',
                                   'PUT, GET, POST, DELETE, HEAD, OPTIONS')
        resp.set_header('Access-Control-Allow-Headers',
                                   'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, X-Auth-Token, Signature')


def loadEndPoints(app, store):
    """
    Add Rest endpoints to a falcon.API object by mapping the API's routes.
    :param app: falcon.API object
    :param store: Store
        ioflo datastore
    """

    survey = surveys.Survey()
    app.add_route('{}/{{id}}'.format(SURVEY_BASE_PATH), survey)
    app.add_route('{}'.format(SURVEY_BASE_PATH), survey)

    log = logs.Logs()
    app.add_route('{}/{{id}}'.format(LOGS_BASE_PATH), log)
    app.add_route('{}'.format(LOGS_BASE_PATH), log)

    csv = csvs.CSV()
    app.add_route('{}'.format(CSVS_BASE_PATH), csv)
