from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Qwerty123@localhost/hw_epam_db'
db =  SQLAlchemy(app)

class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)


def getData(searchStr):
    recData = ()
    # kind, collectionName, trackName, collectionPrice, trackPrice, primaryGenreName, trackCount, trackNumber, releaseDate
    # get artistid all data
     tmp = (requests.get('https://itunes.apple.com/search?term=' + str(searchStr))).json()
    for rec in tmp['results']:
        if rec["artistName"] == searchStr:
            #get records of the Beatles
            recdata.append((rec["artistId"],))  
            return 

@app.route("/")
def index():
     return render_template("index.html", records = getData('The Beatles'))

# Start local project
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
