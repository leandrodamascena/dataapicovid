import json
import boto3
import time

clientedb = boto3.resource('dynamodb', region_name='us-east-1')

# create table APICovid
table = clientedb.create_table(
    TableName='dailyResults',
    KeySchema=[
        {
            'AttributeName': 'country',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'dateTime',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'country',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'dateTime',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait time to proccess dynamodb create table
print("Waiting dynamodb table...")
time.sleep(10)

tableAPICovid = clientedb.Table('dailyResults')

checkNull = lambda x : x if x is not None else 0

print("Inserting data...")
with open('./data/datadaily.json') as json_file:
    data = json.load(json_file)
    for item in data:
        tableAPICovid.put_item(
            Item={
                'country': item['country'],
                'totalCases': checkNull(item['totalCases']),
                'newCases': checkNull(item['newCases']),
                'activeCases': checkNull(item['activeCases']),
                'totalDeaths': checkNull(item['totalDeaths']),
                'newDeaths': checkNull(item['newDeaths']),
                'newRecoveries': checkNull(item['newRecoveries']),
                'dateTime': item['dateTime']
            }
        )

print("Done!")