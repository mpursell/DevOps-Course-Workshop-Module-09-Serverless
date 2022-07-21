import logging
import json
import uuid
import azure.functions as func


def main(msg: func.QueueMessage, messageJSON: str, processedSub: func.Out[str]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    message = json.loads(messageJSON)
    storedSubtitle = message["subtitle"].upper()

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
    return None

