from flask import Flask, render_template, jsonify
import pymongo
import json
from bson import json_util, ObjectId
# from Keys import admin, pw
import urllib.parse
#define app
app = Flask(__name__)

# #DB information
# conn = "mongodb://" +  admin + ":" + urllib.parse.quote_plus(pw) + "@ds121456.mlab.com:21456/heroku_63785bfl"

# client = pymongo.MongoClient(conn)
# db = client.heroku_63785bfl

@app.route("/")
def index():

    return render_template("index.html")

# @app.route("/api/v1/")
# def api():
#     schools = list(db.items.find())

#     return json.dumps(schools, sort_keys=True, indent=4, default=json_util.default)
    
# if __name__ == "__main__":
#     app.run(debug=False)
