from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

import configuration
from logger import logger

app = Flask(__name__)
mongo_uri = "mongodb://{host}:{port}/{database}"
app.config["MONGO_URI"] = mongo_uri.format(host=configuration.HOST, port=configuration.PORT,
                                           database=configuration.DATABASE)
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def home():
    try:
        return jsonify(message="Welcome to Login and Registration app", success=True)
    except Exception as e:
        logger.exception(e)


@app.route('/register/<username>/<password>', methods=['POST', 'GET'])
def register(username, password):
    try:
        if request.method == "GET":
            logger.debug('Wrong method')
            return jsonify(message="Wrong Method", success=False)
        elif request.method == 'POST':
            user = mongo.db.users.find_one({"username": username})
            if user:
                return jsonify(message="Username not available", success=False)
            else:
                mongo.db.users.insert_one(
                    {'username': username, 'password': generate_password_hash(password)})
                return jsonify(message="User Registered", success=True)
    except Exception as e:
        logger.exception(e)


@app.route('/login/<username>/<password>', methods=['POST', 'GET'])
def login(username, password):
    try:
        if request.method == "GET":
            logger.debug('Wrong method')
            return jsonify(message="Wrong Method", success=False)
        elif request.method == 'POST':
            user = mongo.db.users.find_one({"username": username})
            if not user or not check_password_hash(user["password"], password):
                return jsonify(message="Invalid credentials", success=False)
            else:
                return jsonify(message="Login successfull", success=True)
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    logger.debug(app.run())
