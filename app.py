from flask import Flask, render_template, url_for, request
from prometheus_flask_exporter import PrometheusMetrics
import requests
from pymongo import MongoClient
from bson import json_util
import os
import socket
from datetime import datetime

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# default
dbname = "test"
artistname = "test"
colname = "test"
connstr = "test"
fmt = '%Y-%m-%d %H:%M:%S'

try:
    dbname = os.environ['dbname']
    artistname = os.environ['artistname']
    colname = os.environ['colname']
    connstr = os.environ['connstr']
except:
    print("Env vars are not set")

# Connect to db
try:
    client = MongoClient(connstr)
    mydb = client[dbname]
    mycol = mydb[colname]
except:
    print("DB connection failed")

def gettdiff():
   mindate = mycol.find_one(sort=[("date", 1)])["date"]
   try:
      time_delta = (datetime.now() - mindate)
      total_seconds = time_delta.total_seconds()
      return total_seconds/60
   except:
      # if no records
      return 10000000000000
 
def insertdocument(collection, data):
    """ Function to insert a document into a collection and
        return the document's id.
        0. collection - name of collection in DB to safe data
        1. data - portion of data to get recorded
    """
    return collection.insert_one(data).inserted_id

# Get data from remote source
# searchstr - key searching string 
def getdata(searchstr):
    """ Function gets data from remote source and returns total number of records
        0. searchstr - key searching string
    """
    # Total number of records
    totalcount = 0
    # Number of records in JSON
    reccount = 1
    # Records offset
    recoffset = 0
    # Max possible offset - delta
    maxoffset = 200
    # Send request to get data
    while reccount > 0:
        response = (requests.get('https://itunes.apple.com/search?term=' + str(searchstr) + '&offset=' + str(recoffset) + '&limit=' + str(maxoffset-1))).json()
        reccount = response["resultCount"]
        totalcount += reccount 
        recoffset = int(recoffset) + maxoffset
        for onerec in response["results"]:
            onerec["date"] = datetime.now()
            insertdocument(mycol, onerec)
    return totalcount

# Route to Main page
@app.route("/")
def index():
     """ See comment to Route
     """
     return render_template("index.html", ipaddr = socket.gethostbyname(socket.gethostname()), tdiff = gettdiff())

# Route to update DB page
@app.route("/updateall")
def updateall():
     """ See comment to Route
     """
     mydb.drop_collection(mycol)
     return render_template("updateall.html", totalcount = getdata(artistname), ipaddr = socket.gethostbyname(socket.gethostname()), tdiff = gettdiff())

# Route to Output the data by collectionName sorted by relaseDate
@app.route("/display")
def display():
     """ See comment to Route
     """
     result = []
     fulllist = mycol.find({"artistName":artistname})
     distfield = fulllist.distinct("collectionName")
     for el in distfield:
         result.append([mycol.find_one({"collectionName":el, "artistName":artistname})["releaseDate"], el])
     return render_template("display.html", distfield = sorted(result), ipaddr = socket.gethostbyname(socket.gethostname()), tdiff = gettdiff())

# Route to Output all data
@app.route("/displayall", methods=['POST', 'GET'])
def displayall():
     """ See comment to Route
     """
     if request.method == "POST" and (request.form['number']).isdigit():
         recnum = request.form['number']
         fulllist = mycol.find({"artistName":artistname}).limit(int(recnum))
     else:
         fulllist = mycol.find({"artistName":artistname})
     return render_template("displayall.html", fulllist = fulllist, ipaddr = socket.gethostbyname(socket.gethostname()), tdiff = gettdiff())

# Start local project
#if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0')
