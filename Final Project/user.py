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
from flask import Flask, request, jsonify
app = Flask(__name__)

# List of users for testing purposes
all_users = [
    {"id": 1, "name": "UserFoo", "email": "UserFoo@email.com"},
    {"id": 2, "name": "UserJane", "email": "UserJane@email.com"},
    {"id": 3, "name": "UserJohn", "email": "UserJohn@email.com"},
]


# Get user by ID
@app.route("/user/<int:userId>", methods=["GET"])
def user(userId):
    user = None
    for i in all_users:
        if i["id"] == userId:
            user = i
            break
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found.'}), 404

# Create new user


@app.route("/user", methods=["POST"])
def new_user():
    # Get data from the request body
    data = request.json
    userId = len(all_users) + 1
    data["id"] = userId
    all_users.append(data)
    return json.dumps({"message": "New user created succesfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
