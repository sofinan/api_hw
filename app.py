from flask import Flask, render_template, url_for, request
from prometheus_flask_exporter import PrometheusMetrics
import requests
from pymongo import MongoClient
from bson import json_util
import os
import socket

app = Flask(__name__)
metrics = PrometheusMetrics(app)

dbname = os.environ['dbname']
artistname = os.environ['artistname']
colname = os.environ['colname']
connstr = os.environ['connstr']

# Connect to db
client = MongoClient(connstr)
mydb = client[dbname]
mycol = mydb[colname]

def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id

def getData(searchstr):
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
            insert_document(mycol, onerec)
    return totalcount

# Main page
@app.route("/")
def index():
     return render_template("index.html", ipaddr = socket.gethostbyname(socket.gethostname()))

# Drop db and get records
@app.route("/updateall")
def updateall():
     mydb.drop_collection(mycol)
     return render_template("updateall.html", totalcount = getData(artistname), ipaddr = socket.gethostbyname(socket.gethostname()))

# Output the data by collectionName sorted by relaseDate
@app.route("/display")
def display():
     result = []
     fulllist = mycol.find({"artistName":artistname})
     distfield = fulllist.distinct("collectionName")
     for el in distfield:
         result.append([mycol.find_one({"collectionName":el, "artistName":artistname})["releaseDate"], el])
     return render_template("display.html", distfield = sorted(result), ipaddr = socket.gethostbyname(socket.gethostname()))

# Output all data
@app.route("/displayall", methods=['POST', 'GET'])
def displayall():
     if request.method == "POST" and (request.form['number']).isdigit():
         recnum = request.form['number']
         fulllist = mycol.find({"artistName":artistname}).limit(int(recnum))
     else:
         fulllist = mycol.find({"artistName":artistname})
     return render_template("displayall.html", fulllist = fulllist, ipaddr = socket.gethostbyname(socket.gethostname()))

# Start local project
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
