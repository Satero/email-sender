from chalice import Chalice
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

import boto3
import random
import csv
import time
import os

app = Chalice(app_name="emailsender")
app.debug = True

client = boto3.client("ses")
reasons = "Reasons"

dynamodb_resource = boto3.resource("dynamodb", region_name="us-west-2",
                                   endpoint_url="https://dynamodb.us-"
                                   + "west-2.amazonaws.com")
dynamodb_client = boto3.client("dynamodb", region_name="us-west-2",
                               endpoint_url="https://dynamodb.us-"
                               + "west-2.amazonaws.com")

if reasons not in dynamodb_client.list_tables()["TableNames"]:
    dynamodb_client.create_table(
        TableName=reasons,
        KeySchema=[
            {
                "AttributeName": "ID",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "Reasons",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "ID",
                "AttributeType": "N"
            },
            {
                "AttributeName": "Reasons",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    )
    time.sleep(15)  # Allows time for server to create table.

    reasons_table = dynamodb_resource.Table(reasons)

    with open("Reasons.csv", "r") as csvfile:
        reasons_file = csv.reader(csvfile, delimiter=" ")
        counter = 0
        for reason in reasons_file:
            table.put_item(
                Item={
                    "ID": counter,
                    "Reasons": " ".join(reason)
                }
            )

            counter += 1


@app.schedule(Rate(1, unit=Rate.HOURS))
def email_lambda_function(event):
    try:
        reasons_table = dynamodb_resource.Table(reasons)
        rand_int = random.randint(0, 25)
        response = table.query(KeyConditionExpression=Key("ID").eq(rand_int))
        client.send_email(
            Destination={
                "ToAddresses": [os.environ['RECEIVER_1']]
                + [os.environ['RECEIVER_2']]
            },
            Message={
                "Body": {
                    "Text": {
                        "Data": response["Items"][0]["Reasons"]
                    }
                },
                "Subject": {
                    "Data": "Another reason why you should hire Justin Picar."
                }
            },
            Source=os.environ['SENDER']
        )
    except ClientError as c:
        app.log.error(c)


@app.route("/")
def index():
    pass
