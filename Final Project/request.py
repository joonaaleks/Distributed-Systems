##############################
# Distributed Systems Final Project
# Author: Joona Pellinen
# Date: 28.4.2023
# Sources:
# https://www.linode.com/docs/guides/create-restful-api-using-python-and-flask/
# https://pythonbasics.org/flask-rest-api/
# https://www.analyticsvidhya.com/blog/2022/01/rest-api-with-python-and-flask/
# https://pythonbasics.org/flask-tutorial-routes/
# Course Material
###############################

import json
from flask import Flask, request
app = Flask(__name__)

# List of drivers for testing purposes
all_drivers = [
    {"id": 1, "name": "DriverFoo", "available": False},
    {"id": 2, "name": "DriverJane", "available": False},
    {"id": 3, "name": "DriverJohn", "available": False},
]


@app.route("/request", methods=["POST"])
def req():
    # Get data from the request body
    data = request.json
    passengerId = data["passengerId"]
    pickup_location = data["start"]
    destination = data["end"]

    set_driver = None
    for driver in all_drivers:
        if driver["available"]:
            set_driver = driver
            break

    if set_driver:
        set_driver["available"] = False

        # Response body
        ride_request_response = {
            "driverId": set_driver["id"],
            "driverName": set_driver["name"],
            "passenger": passengerId,
            "pickupLocation": pickup_location,
            "destination": destination
        }

        return json.dumps(ride_request_response), 200
    else:
        return json.dumps({"message": "No available drivers."}), 404


if __name__ == "__main__":
    app.run(debug=True)
