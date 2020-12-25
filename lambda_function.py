#
# Lambda function used to write inbound IoT sensor data to RDS PostgeSQL database
#
# !/usr/bin/python
import json
#import boto3
import psycopg2
import logging

db_host = "aai8sv1pv4yyiu.ccqnqsv9nq4a.eu-central-1.rds.amazonaws.com"
db_port = 5432
db_name = "ebdb"
db_user = "pgadmin"
db_pass = "Mnv7711021106"
db_table = "mainpage_status"


def record(event, context):
    try:
        conn = psycopg2.connect(host="aai8sv1pv4yyiu.ccqnqsv9nq4a.eu-central-1.rds.amazonaws.com",
                                port="5432",
                                dbname="ebdb",
                                user="pgadmin",
                                password="Mnv7711021106")
        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(
            'insert into "mainpage_status" (timestamp, current_moisture, target_moisture, mode, relay_target_status, relay_current_state) '
            'values (%s, %s, %s, %s, %s, %s)',
            (event['timestamp'], event['current moisture'], event['target moisture'], event['mode'],
             event['relay target status'], event['relay_current_state']))
        cur.close()

    # No except statement is used since any exceptions should fail the function so that the
    # failed message is sent to the SQS destination configured for the Lambda function
    finally:
        try:
            conn.close()
        except:
            pass


def lambda_handler(event, context):
    # Parse the JSON message
    eventText = json.dumps(event)
    if 'mode' not in eventText:
        logging.error("Validation Failed - no mode parameter in message")
        raise Exception("Validation Failed - no mode parameter in message")
    elif 'current moisture' not in eventText:
        logging.error("Validation Failed - no current moisture parameter in message")
        raise Exception("Validation Failed - no current moisture parameter in message")
    elif 'target moisture' not in eventText:
        logging.error("Validation Failed - no target moisture parameter in message")
        raise Exception("Validation Failed - no target moisture parameter in message")
    elif 'relay target status' not in eventText:
        logging.error("Validation Failed - no relay target status parameter in message")
        raise Exception("Validation Failed - no relay target status parameter in message")
    elif 'relay_current_state' not in eventText:
        logging.error("Validation Failed - no relay_current_state parameter in message")
        raise Exception("Validation Failed - no relay_current_state parameter in message")
    elif 'timestamp' not in eventText:
        logging.error("Validation Failed - no timestamp parameter in message")
        raise Exception("Validation Failed - no timestamp parameter in message")
    else:
        record(event, context)

    # TODO implement
    return {
        'statusCode': 200,
        'body': eventText
    }
# Used when testing from the Linux command line
"""
if __name__ == "__main__":
    event = {
        "current moisture": 0,
        "target moisture": 400,
        "mode": "auto",
        "relay target status": "on",
        "relay_current_state": "on",
        "timestamp": 1608485393
    }
    handler(event=event, context=None)
"""
