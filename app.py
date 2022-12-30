import io
from flask import Flask, render_template, send_file, request, jsonify, send_file
from collections import deque
import numpy as np 
import pandas as pd 
import math 
import os

app = Flask(__name__)

# Initialize empty global dataframe
df = pd.DataFrame.from_dict({})
place_idx = 0 

# REMOVED TYPES BECAUSE RESTAURANTS DON'T HAVE THEM IN THE CSV FOR SOME REASON 
columns = ["Name", "Address", "Lat", "Lon", "Type", "Business_Status", "Icon", "Price_Level", "Rating", "ID", "Photo Reference"]

# Initialize df to store content that we want to keep 
df_keep = pd.DataFrame(columns = columns)

# Initialize df to store content that we want to delete 
df_delete = pd.DataFrame(columns = columns)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/places')
def places():
    return render_template('places.html')

# Extract the input image and save its content in the gloval dataframe
@app.route('/extract', methods=["POST"])
def extract():
    global df 

    # Store the file
    in_file = request.files['csv']

    # Parse the file into global dataframe
    df = pd.read_csv(in_file)

    # Replace NaNs with N/A
    df.fillna('N/A', inplace=True)

    return render_template('places.html')

# Send json of place data at current idx
@app.route('/place', methods=["GET"])
def place():
    global place_idx
    global columns

    place = {}

    for item in columns: 
      place[item] = df.loc[place_idx, item]

    return jsonify(place), 200

# Add place to df_keep 
@app.route('/keep', methods=["POST"])
def keep():
    global df_keep
    global columns 

    row = []

    for item in columns: 
        row.append(df.loc[place_idx, item])

    df_keep = df_keep.append(row)

    return "Done", 200

# Add place to df_delete 
@app.route('/delete', methods=["POST"])
def delete():
    global df_delete
    global columns

    row = []

    for item in columns: 
        row.append(df.loc[place_idx, item])

    df_delete = df_delete.append(row)

    return "Done", 200

# Get next item in df 
@app.route('/next', methods=["POST"])
def next():
    global place_idx
    place_idx += 1
    return "Done", 200

# Get prev item in df 
@app.route('/previous', methods=["POST"])
def previous():
    global place_idx
    place_idx -= 1
    return "Done", 200

# Send csv file of places to keep 
@app.route('/data_keep', methods=["GET"])
def data_keep():
    global df_keep

    caldf = df_keep.to_csv(index=False, header=True)
    buf_str = io.StringIO(caldf)
    return send_file (io.BytesIO(buf_str.read().encode("utf-8")), mimetype="text/csv", attachment_filename="data.csv")

# Send csv file of places to keep 
@app.route('/data_delete', methods=["GET"])
def data_delete():
    global df_delete

    caldf = df_delete.to_csv(index=False, header=True)
    buf_str = io.StringIO(caldf)
    return send_file (io.BytesIO(buf_str.read().encode("utf-8")), mimetype="text/csv", attachment_filename="data.csv")


