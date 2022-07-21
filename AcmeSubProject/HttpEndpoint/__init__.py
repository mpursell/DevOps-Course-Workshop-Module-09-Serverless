import logging
import time
import uuid
import json
import typing
import azure.functions as func


def main(request: func.HttpRequest, message: func.Out[str], msg: func.Out[typing.List[str]]) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')

    request_body = request.get_json()
    subtitle = request_body.get("subtitle")
    languages = request_body.get("languages")


    rowKey = str(uuid.uuid4())

    data = {
        "Name": "message",
        "PartitionKey": "message",
        "RowKey": rowKey,
        "subtitle": subtitle,
        "languages": languages
    }

    message.set(json.dumps(data))
    
    # add a message to the queue for each language
    languageList = []
    for language in languages:

        queueData ={
            "Name": "msg",
            "language": language,
            "RowKey": rowKey
        }

        languageList.append(json.dumps(queueData))

    msg.set(languageList)
    ##

    return func.HttpResponse(f"Message created with the rowKey: {rowKey}")
    
