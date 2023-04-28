##############################
# Distributed Systems Final Project
# Author: Joona Pellinen
# Date: 28.4.2023
# Sources:
# https://www.linode.com/docs/guides/create-restful-api-using-python-and-flask/
# https://pythonbasics.org/flask-rest-api/
# https://www.analyticsvidhya.com/blog/2022/01/rest-api-with-python-and-flask/
# https://pythonbasics.org/flask-tutorial-routes/
# https://www.youtube.com/watch?v=dFbmAIglaVM
# Course Material
###############################
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

# List of drivers for testing purposes
all_drivers = [
    {"id": 1, "name": "DriverFoo", "available": True},
    {"id": 2, "name": "DriverJane", "available": False},
    {"id": 3, "name": "DriverJohn", "available": True},
]

# GET all drivers


@app.route("/driver", methods=["GET"])
def users():
    return jsonify(all_drivers)

# Create new driver


@app.route("/driver", methods=["POST"])
def new_driver():
    # Get data from the request body
    data = request.json
    driverId = len(all_drivers) + 1
    data["id"] = driverId
    data["available"] = True
    all_drivers.append(data)
    return json.dumps({"message": "New driver created succesfully!"}), 200

# Delete driver


@app.route("/driver/<int:driverId>", methods=["DELETE"])
def delete_driver(driverId):
    for i in all_drivers:
        if driverId == i["id"]:
            all_drivers.remove(i)
            return json.dumps({"message": "Driver deleted"}), 200
    return json.dumps({"message": "Driver not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
