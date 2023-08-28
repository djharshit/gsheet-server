"""
Python script to save the data sent by the client to a csv file on the server side using Flask framework
"""
import csv
from threading import RLock

from flask import Flask, jsonify, request

app = Flask(__name__)

file = open("data.csv", "a", newline="")
csv_writer = csv.writer(file)
rlock = RLock()


@app.route("/")
def home_page():
    """
    Home page of the server
    """

    return "Hello, World!"


@app.post("/add")
def add_row():
    """
    Add a row to the csv file on the server side using the data sent by the client
    """

    try:
        data = request.get_json()

        print(data)  # For debugging

        rlock.acquire()

        csv_writer.writerow([data["fullName"], data["phoneNumber"], data["homeTown"], data["email"], data["branch"]])
        file.flush()

        rlock.release()

        return jsonify({"status": "success"})

    except Exception as e:
        print(e)  # For debugging

        return jsonify({"status": "failure"}), 400


if __name__ == "__main__":
    print("Server starting...")
    app.run(host="0.0.0.0", port=5000, debug=True)
