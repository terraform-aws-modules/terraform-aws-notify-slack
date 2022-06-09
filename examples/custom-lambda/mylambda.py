#!/usr/bin/python3.6
# CUSTOM LAMBDA FUNCTION

import urllib3
import json
import os
http = urllib3.PoolManager()


def lambda_handler(event, context):
    url = os.environ["SLACK_WEBHOOK_URL"]
    msg = {
        "channel": "#channel-name",
        "username": "Prometheus",
        "text": event['Records'][0]['Sns']['Message'],
        "icon_emoji": ""
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
    print({
        "message": event['Records'][0]['Sns']['Message'],
        "status_code": resp.status,
        "response": resp.data
    })
