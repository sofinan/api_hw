from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Qwerty123@localhost/hw_epam_db'
db =  SQLAlchemy(app)

class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


# Start local project
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
