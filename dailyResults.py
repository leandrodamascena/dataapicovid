#from app import app
from flask import request, jsonify
import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

class dailyResults:

    def countryDailyResultsRest(country=None,datetime=None):

        clientedb = boto3.resource('dynamodb', region_name='us-east-1')

        tabledb = clientedb.Table('dailyResults')

        #returning all countries if country and datetime are empty
        if country is None and datetime is None:
            return json.loads(json.dumps(tabledb.scan(), cls=DecimalEncoder))
        
        #returning data specified by country
        if country is not None and datetime is None:
            datacountry = tabledb.query(
                Select='ALL_ATTRIBUTES',
                ConsistentRead=False,
                KeyConditionExpression=Key('country').eq(country)
            )
            if datacountry['Count'] == 0:
                return jsonify({'message': "there is no data to country " + country}), 200
            else:
                return json.loads(json.dumps(datacountry, cls=DecimalEncoder))
        
        #returning data specified by country and initial date
        if country is not None and datetime is not None:
            datacountrytime = tabledb.query(
                Select='ALL_ATTRIBUTES',
                ConsistentRead=False,
                KeyConditionExpression=Key('country').eq(country) & Key('dateTime').gt(datetime)
            )
            if datacountrytime['Count'] == 0:
                return jsonify({'message': "there is no data to country " + country + " and initial data " + datetime}), 200
            else:
                return json.loads(json.dumps(datacountrytime, cls=DecimalEncoder))