#!/usr/bin/env python3

"""
Python script to save the data sent by the client to a csv file on the server side using Flask framework
"""
import csv
from threading import RLock
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

file = open("data.csv", "a", newline="")
csv_writer = csv.writer(file)
rlock = RLock()


@app.route("/")
@cross_origin()
def home_page():
    """
    Home page of the server
    """

    return "Hello, World!"


@app.post("/add")
@cross_origin()
def add_row():
    """
    Add a row to the csv file on the server side using the data sent by the client
    """

    try:
        data = request.form.to_dict()

        print(data)  # For debugging

        rlock.acquire()

        csv_writer.writerow(
            [
                datetime.now(),
                data["fullName"],
                data["phoneNumber"],
                data["homeTown"],
                data["email"],
                data["branch"],
                data["teamsInterested"],
                data["pastExp"],
                data["whyJoin"],
            ]
        )
        file.flush()

        rlock.release()

        return jsonify({"status": "success"})

    except Exception as e:
        print(e)  # For debugging

        return jsonify({"status": "failure"}), 400


if __name__ == "__main__":
    print("Server starting...")
    app.run(host="0.0.0.0", port=80, debug=True)
