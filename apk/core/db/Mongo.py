import os
import logging
import traceback
from pymongo import MongoClient, HASHED
from ConfigParser import ConfigParser
from bson.objectid import ObjectId

class DB():
    def __init__(self):
        #def __init__(self,config_name = 'test'):
        #config_name = 'TEST'
        #parser = ConfigParser()
        #config_file = os.path.dirname(__file__)+"/db.conf"
        #parser.read(config_file)
        #db_server = parser.get(config_name,'ip')
        #db_name = parser.get(config_name,'database')
        try:
            connection = MongoClient('localhost:27017')
            self.db = connection.apk

            # Use MongoClient to create a connection
        except:
            logging.error("DB connect error!")
        #finally:
            #logging.debug("Using DB server: {0},DB: {1}".format(db_server,db_name))
    def get_apk_info(self):
        result = self.db.apk.find_one()
        print "apk info : ",result
    def insert_apk(self,origin_payload):
        payload = origin_payload #not yet to check column
        #payload = self._clean_query(origin_payload)
        #if self.fs.exists({'filename' : payload['sha512']}):
        #    print "File already exists!"
        #    logging.debug("{0} File already exists!".format(payload['pgname']))
        #    file_id = self.fs.find_one({'filename':payload['sha512']})._id
        #else:
        #    file_id = self.fs.put(payload['apkdata'],filename = payload['sha512'])
        #payload['apkdata'] = file_id

        try:
            payload['_id']=ObjectId()
            self.db.apk.insert_one(payload)
        except Exception,e:
            traceback.print_exc()
            print "Error insert data!"
