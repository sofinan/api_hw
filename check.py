from pymongo import MongoClient
from datetime import datetime
import os
import requests
from bson import json_util
import socket
from app import getdata,countRecords 

# default
dbname = "test"
artistname = "test"
colname = "test"
connstr = "test"
fmt = '%Y-%m-%d %H:%M:%S'
updateperiod = 5

try:
    dbname = os.environ['dbname']
    artistname = os.environ['artistname']
    colname = os.environ['colname']
    connstr = os.environ['connstr']
except:
    print("Env vars are not set")

def insertdocument(collection, data):
    """ Function to insert a document into a collection and
        return the document's id.
        0. collection - name of collection in DB to safe data
        1. data - portion of data to get recorded
    """
    return collection.insert_one(data).inserted_id

# Connect to db
try:
    client = MongoClient(connstr)
    mydb = client[dbname]
    mycol = mydb[colname]
except:
    print("DB connection failed")

mindate = mycol.find_one(sort=[("date", 1)])["date"]

try:
   time_delta = (datetime.now() - mindate)
   total_seconds = time_delta.total_seconds()
   minutes = total_seconds/60
except:
   # if no records
   minutes = 10000000000000

print(minutes)
if minutes > updateperiod:
   numsrcrec = countRecords(artistname)
   numdbrec = mycol.count()
   print(numsrcrec, numdbrec)
   currdt = datetime.now()
   mycol.update_many(
      { },
        {
            "$set": {"date" : currdt }
        },
   upsert=False,
   array_filters=None
   )
   if numsrcrec != numdbrec:
      mydb.drop_collection(mycol)
      print("dropped")
      totalcount = getdata(artistname)
      print(totalcount)
