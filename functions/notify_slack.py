from __future__ import print_function
import os, boto3, json, base64
import urllib.request, urllib.parse
import logging

def decrypt(encrypted_url):
    """
    Decrypt encrypted URL with KMS
    """
    region = os.environ['AWS_DEFAULT_REGION']
    try:
        kms = boto3.client('kms', region_name=region)
        plaintext = kms.decrypt(CiphertextBlob=base64.b64decode(encrypted_url))['Plaintext']
        return plaintext.decode()
    except Exception:
        logging.exception("Failed to decrypt URL with KMS")

def notify_slack(message):
    """
    Send a message to a slack channel
    """
    slack_url = os.environ['SLACK_WEBHOOK']
    if not slack_url.startswith("http"):
        slack_url = decrypt(slack_url)

    slack_channel = os.environ['SLACK_CHANNEL']
    
    text = message['AlarmName']
    states = {'OK' : 'good', 'INSUFFICIENT_DATA': 'warning', 'ALARM': 'danger'}
    
    payload = {
        "channel": slack_channel,
        "username": "AWS Cloudwatch",
        "text": text,
        "color": states[message['NewStateValue']]
    }

    data = urllib.parse.urlencode({"payload":json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(slack_url)
    response = urllib.request.urlopen(req, data)

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    notify_slack(message)
    return message

# notify_slack({'AlarmName': "Hello", "NewStateValue": "OK"})