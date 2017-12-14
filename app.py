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

"""AWS DynamoDB checks to see if a table "Reasons" exists.
If not, it creates a new table called "Reasons", and
populates it with information from Reasons.csv.

"""
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

    # This holds the code from running, giving
    # time for the server to create the table.
    time.sleep(15)

    reasons_table = dynamodb_resource.Table(reasons)

    with open("Reasons.csv", "r") as csvfile:
        reasons_file = csv.reader(csvfile, delimiter=" ")
        counter = 0
        for reason in reasons_file:
            reasons_table.put_item(
                Item={
                    "ID": counter,
                    "Reasons": " ".join(reason)
                }
            )

            counter += 1


@app.schedule('rate(1 hour)')
def email_lambda_function(event):
    """AWS Lambda function that pulls from the "Reasons" DynamoDB table
    and uses SES to send an email.

    The decorator is an indicator for CloudWatch to create a rule and
    schedule an event for this Lambda function to run every hour.

    """
    try:
        reasons_table = dynamodb_resource.Table(reasons)
        rand_int = random.randint(0, 25)
        response = reasons_table.query(
            KeyConditionExpression=Key("ID").eq(rand_int))
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
    """AWS Chalice app requires one function to use the above decorator
    as a default. Otherwise, this function serves no purpose.

    """
    pass
