from flask import Flask, render_template, jsonify
import pymongo
import json
from bson import json_util, ObjectId

#define app
app = Flask(__name__)

#DB information
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.syria_db

@app.route("/")
def index():
    schools = list(db.items.find())

    return render_template("index.html", schools=schools)

@app.route("/api/v1/")
def api():
    schools = list(db.items.find())

    return json.dumps(schools, sort_keys=True, indent=4, default=json_util.default)
    
if __name__ == "__main__":
    app.run(debug=True)
