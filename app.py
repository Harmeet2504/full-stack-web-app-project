from flask import Flask, render_template
# from flask_table import Table, Col
from flask_pymongo import PyMongo
from flask import jsonify
from flask import request
import json

import dns

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://Harmeet:harmeet123@cluster0-v6uxh.mongodb.net/complete_death_coord_data"
mongo = PyMongo(app)


@app.route("/")
def index():
    collection = mongo.db.mortality_records.find_one()
    return render_template("index.html", collection=collection)

##########Route that returns complete data##################
@app.route('/api/v1.0/data/', methods=['GET'])
def data():
  """Return the complete data"""
  deaths = mongo.db.mortality_records
  output = []
  for s in deaths.find():
    output.append({'year' : s['year'],'cause_name' : s['cause_name'],'state' : s['state'],'deaths' : s['deaths'],'aadr' : s['aadr'], 'Latitude' : s['Latitude'], 'Longitude' : s['Longitude']})
  return jsonify({'result' : output})
############################################################

#######Route to return metadata for a year####################
@app.route("/api/v1.0/metadata/<year>", methods=['GET'])
def sample_yearData(year):
    """Return the MetaData for a given year."""
    query = year
    data=mongo.db.mortality_records.find({"year": query})
    years_output = []
    for i in data:
        years_output.append({'year' : i['year'],'cause_name' : i['cause_name'],'state' : i['state'],'deaths' : i['deaths']})
    return jsonify({'result' : years_output})
###############################################################

#######Route to return metadata for a state####################
@app.route("/api/v1.0/<state>", methods=['GET'])
def sample_stateData(state):
    """Return the MetaData for a given state."""
    query = state
    state_data=mongo.db.mortality_records.find({"state": query})
    state_output = []
    for i in state_data:
        state_output.append({'state' : i['state'],'cause_name' : i['cause_name'],'deaths' : i['deaths'],'year' : i['year']})
    return jsonify({'result' : state_output})
###############################################################

@app.route('/causes', methods=['GET'])
def causes():
  deaths = mongo.db.mortality_records
  output = []
#   myquery = { "year": "2017" }

#   for s in deaths.find(myquery):
  for s in deaths.find():
    output.append({'year' : s['year'],'cause_name' : s['cause_name'],'state' : s['state'],'deaths' : s['deaths'],'aadr' : s['aadr'], 'Latitude' : s['Latitude'], 'Longitude' : s['Longitude']})
  return jsonify({'result' : output})



if __name__ == "__main__":
    app.run(debug=True)