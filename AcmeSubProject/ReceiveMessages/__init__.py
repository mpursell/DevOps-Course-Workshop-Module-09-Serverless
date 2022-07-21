import logging
import json
import uuid
import dotenv
import os
import requests
import azure.functions as func

def translate(text: str, languageCode: str):

    # Add your key and endpoint
    dotenv.load_dotenv()
    key: str = os.getenv("TRANSLATOR_API_KEY")
    endpoint: str = os.getenv("TRANSLATOR_ENDPOINT")

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "westeurope"

    path = '/translate'
    constructed_url: str = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': languageCode
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))


def main(msg: func.QueueMessage, messageJSON: str, processedSub: func.Out[str]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    message = json.loads(messageJSON)
    storedSubtitle = message["subtitle"]

    msgBody = msg.get_body().decode('utf-8')
    msgJson = json.loads(msgBody)
    languageCode = msgJson["language"]

    rowKey = str(uuid.uuid4())

    data = {
        "Name": "subtitle",
        "PartitionKey": "subtitle",
        "RowKey": rowKey,
        "subtitle": storedSubtitle,
        "language": languageCode
    }

    processedSub.set(json.dumps(data))

    logging.info(message["subtitle"])

    translate(storedSubtitle, languageCode)
    return None

