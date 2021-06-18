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
artistname = os.environ['artistName']
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

def getData(searchStr):
    # Total number of records
    totalCount = 0
    # Number of records in JSON
    recCount = 1
    # Records offset
    recOffset = 0
    # Max possible offset - delta
    maxOffset = 200
    # Send request to get data
    while recCount > 0:
        response = (requests.get('https://itunes.apple.com/search?term=' + str(searchStr) + '&offset=' + str(recOffset) + '&limit=' + str(maxOffset-1))).json()
        recCount = response["resultCount"]
        totalCount += recCount 
        recOffset = int(recOffset) + maxOffset
        for oneRec in response["results"]:
            insert_document(mycol, oneRec)
    return totalCount

# Main page
@app.route("/")
def index():
     return render_template("index.html", ipaddr = socket.gethostbyname(socket.gethostname()))

# Drop db and get records
@app.route("/updateall")
def updateall():
     mydb.drop_collection(mycol)
     return render_template("updateall.html", totalCount = getData(artistname), ipaddr = socket.gethostbyname(socket.gethostname()))

# Output the data by collectionName sorted by relaseDate
@app.route("/display")
def display():
     result = []
     fullList = mycol.find({"artistname":artistname})
     distField = fullList.distinct("collectionName")
     for el in distField:
         result.append([mycol.find_one({"collectionName":el, "artistName":artistName})["releaseDate"], el])
     return render_template("display.html", distField = sorted(result), ipaddr = socket.gethostbyname(socket.gethostname()))

# Output all data
@app.route("/displayall", methods=['POST', 'GET'])
def displayall():
     if request.method == "POST" and (request.form['number']).isdigit():
         recNum = request.form['number']
         fullList = mycol.find({"artistName":artistName}).limit(int(recNum))
     else:
         fullList = mycol.find({"artistName":artistName})     
     return render_template("displayall.html", fullList = fullList, ipaddr = socket.gethostbyname(socket.gethostname()))

# Start local project
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
