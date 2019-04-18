from flask import Flask, request
import json
import requests
import os
from . import bot

PAT = os.environ.get('PAT', None)
verify_token = os.environ.get('VERIFY_TOKEN', None)

@bot.route('/', methods=['GET'])
def verification():
    if PAT is not None and verify_token is not None:
        if request.args.get('hub.verify_token', '') == verify_token:
            print("Verification successful!")
            return request.args.get('hub.challenge', '')
        else:
            print("Verification failed!")
            return 'Error, wrong validation token'
    else:
        return "Could not get verification tokens."


@bot.route('/', methods=['POST'])
def StartMessaging():
    try:
        if messages['object'] == 'page':
            for message in messages['entry']:
                for msg in message['messaging']:
                    if (msg.get('message')) or  (msg.get('postback')):
                        print(msg)
    except Exception as e:
        raise e


    return 'OK', 200
