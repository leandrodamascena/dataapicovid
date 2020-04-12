from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask import jsonify
from datetime import date
import datetime  
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from werkzeug.exceptions import *
from dailyResults import *
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

#xray_recorder.configure(dynamic_naming='*.apicovid')

#Flask definitions
app = Flask(__name__)

@app.errorhandler(Exception)
def exception_handler(error):
	return jsonify({'errorCode' : 500, 'message' : repr(error)}), 500

api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Configurations
app.config.from_object('config')

#Debug xray na AWS
xray_recorder.configure(service='APP ApiCOVID')
XRayMiddleware(app, xray_recorder)
patch_all()

__prefix__ = "/"

@app.route(__prefix__ + 'countryDailyResults', methods=['GET'])
@app.route(__prefix__ + 'countryDailyResults/<string:country>', methods=['GET'])
@app.route(__prefix__ + 'countryDailyResults/<string:country>/<string:datetime>', methods=['GET'])
def countryDailyResults(country=None,datetime=None):
    return dailyResults.countryDailyResultsRest(country, datetime)

@app.route('/')
def index():

    cur_path = os.path.dirname(__file__)
    f = open(cur_path + '/zen.txt')

    return jsonify({'message': "Hello my friend.. keep calm, breath and read Python Manifest..." + f.read()})

