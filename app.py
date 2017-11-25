from flask import Flask, render_template, jsonify
import pymongo
import json
from bson import json_util, ObjectId
import Keys
import urllib 
#define app
app = Flask(__name__)


#DB information
conn = "mongodb://" +  Keys.admin + ":" + urllib.parse.quote_plus(Keys.pw) + "@ds121456.mlab.com:21456/heroku_63785bfl"

client = pymongo.MongoClient(conn)
db = client.get_default_database()

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/api/v1/")
def api():
    schools = list(db.items.find())

    return json.dumps(schools, sort_keys=True, indent=4, default=json_util.default)
    
if __name__ == "__main__":
    app.run(debug=False)
