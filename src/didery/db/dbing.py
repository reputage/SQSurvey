import lmdb
import os
try:
    import simplejson as json
except ImportError:
    import json


MAX_DB_COUNT = 8

DATABASE_DIR_PATH = "/var/sqsurvey/db"
ALT_DATABASE_DIR_PATH = os.path.join('~', '.consensys/sqsurvey/db')

DB_SURVEY_RESULTS_NAME = b'survey_results'
DB_LOG_NAME = b'log'

gDbDirPath = None   # database directory location has not been set up yet
SQSurveyDB = None    # database environment has not been set up yet
surveyDB = None
logDB = None


def setupDbEnv(baseDirPath=None, port=8080):
    """
    Setup the module globals gDbDirPath, and SQSurveyDB using baseDirPath
    if provided otherwise use DATABASE_DIR_PATH
    :param port: int
        used to differentiate dbs for multiple SQSurvey servers running on the same computer
    :param baseDirPath: string
        directory where the database is located
    """
    global gDbDirPath, SQSurveyDB, surveyDB

    if not baseDirPath:
        baseDirPath = "{}{}".format(DATABASE_DIR_PATH, port)

    baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
    if not os.path.exists(baseDirPath):
        try:
            os.makedirs(baseDirPath)
        except OSError as ex:
            baseDirPath = "{}{}".format(ALT_DATABASE_DIR_PATH, port)
            baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
            if not os.path.exists(baseDirPath):
                os.makedirs(baseDirPath)
    else:
        if not os.access(baseDirPath, os.R_OK | os.W_OK):
            baseDirPath = "{}{}".format(ALT_DATABASE_DIR_PATH, port)
            baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
            if not os.path.exists(baseDirPath):
                os.makedirs(baseDirPath)

    gDbDirPath = baseDirPath  # set global

    SQSurveyDB = lmdb.open(gDbDirPath, max_dbs=MAX_DB_COUNT)
    SQSurveyDB.open_db(DB_SURVEY_RESULTS_NAME)
    SQSurveyDB.open_db(DB_LOG_NAME)

    surveyDB = BaseSurveyDB()

    return SQSurveyDB


class DB:
    def __init__(self, namedDB):
        """
        :param namedDB: string
            name of the table to be accessed
        """
        self.namedDB = namedDB

    def count(self):
        """
            Gets a count of the number of entries in the table

            :return: int count
        """
        subDb = SQSurveyDB.open_db(self.namedDB)

        with SQSurveyDB.begin(db=subDb, write=False) as txn:
            return txn.stat(subDb)['entries']

    def save(self, key, data):
        """
            Store a key value pair

            :param key: string
                key to identify data
            :param data: dict
                A dict of the data to be stored

        """
        subDb = SQSurveyDB.open_db(self.namedDB)

        with SQSurveyDB.begin(db=subDb, write=True) as txn:
            txn.put(
                key.encode(),
                json.dumps(data).encode()
            )

    def get(self, key):
        """
            Find and return a key value pair

            :param key: string
                key to look up
            :return: dict
        """
        subDb = SQSurveyDB.open_db(self.namedDB)

        with SQSurveyDB.begin(db=subDb, write=False) as txn:
            raw_data = txn.get(key.encode())

            if raw_data is None:
                return None

            return json.loads(raw_data)

    def getAll(self, offset=0, limit=10):
        """
            Get all key value pairs in a range between the offset and offset+limit

            :param offset: int starting point of the range
            :param limit: int maximum number of entries to return
            :return: dict
        """
        subDb = SQSurveyDB.open_db(self.namedDB)
        values = {"data": {}}

        with SQSurveyDB.begin(db=subDb, write=False) as txn:
            cursor = txn.cursor()

            count = 0
            for key, value in cursor:
                if count >= limit+offset:
                    break

                if offset < count+1:
                    values["data"][key] = json.loads(value)

                count += 1

        return values

    def delete(self, key):
        """
            Find and delete a key value pair matching the supplied key.

            :param key: string
                key to delete
            :return: boolean
        """
        subDb = SQSurveyDB.open_db(self.namedDB)

        with SQSurveyDB.begin(db=subDb, write=True) as txn:
            status = txn.delete(key.encode())

            return status


class BaseSurveyDB:
    def __init__(self, db=None):
        """
            :param db: DB for interacting with lmdb
        """
        if db is None:
            self.db = DB(DB_SURVEY_RESULTS_NAME)
        else:
            self.db = db

    def count(self):
        """
            Returns the number of entries in the table

            :return: int count
        """
        return self.db.count()

    def save(self, id, data):
        """
            Store a survey response

            :param id: string
                ip address
            :param data: dict
                A dict containing the survey response

        """
        self.db.save(id, data)

        return data

    def get(self, id):
        """
            Find and return a survey response matching the supplied id.

            :param id: string
                ip address connected to the survey response
            :return: dict
        """
        return self.db.get(id)

    def getAll(self, offset=0, limit=10):
        """
            Get all survey responses in a range between the offset and offset+limit

            :param offset: int starting point of the range
            :param limit: int maximum number of entries to return
            :return: dict
        """
        return self.db.getAll(offset, limit)

    def delete(self, id):
        """
            Find and delete a survey response matching the supplied id.

            :param id: string
                ip address connected to the survey response
            :return: boolean
        """
        return self.db.delete(id)


class BaseLogDB:
    def __init__(self, db=None):
        """
            :param db: DB for interacting with lmdb
        """
        if db is None:
            self.db = DB(DB_LOG_NAME)
        else:
            self.db = db

    def count(self):
        """
            Returns the number of entries in the table

            :return: int count
        """
        return self.db.count()

    def save(self, id, data):
        """
            Store a survey response

            :param id: string
                ip address
            :param data: dict
                A dict containing the survey response

        """
        self.db.save(id, data)

        return data

    def get(self, id):
        """
            Find and return a survey response matching the supplied id.

            :param id: string
                ip address connected to the survey response
            :return: dict
        """
        return self.db.get(id)

    def getAll(self, offset=0, limit=10):
        """
            Get all survey responses in a range between the offset and offset+limit

            :param offset: int starting point of the range
            :param limit: int maximum number of entries to return
            :return: dict
        """
        return self.db.getAll(offset, limit)

    def delete(self, id):
        """
            Find and delete a survey response matching the supplied id.

            :param id: string
                ip address connected to the survey response
            :return: boolean
        """
        return self.db.delete(id)
