from flask import Flask, request
import json
import requests

from . import bot



PAT = 'EAAarLkMVMy4BAMKvoGqRqod35PTLNIh6NHjVjKBOiqL3jnVAjBXfwPvXpA5WMJQsstY3VePK8J7jEuGt7ifXC8R0QwvYs05oGRk4JnghiIB2xmZCbsDoLphimTk6vEwe4aYCYTlpBFxIpbZBVSdJGZCl4ZCELZBLiHzhYFJDipQZDZD'
VerifyToken = 'jumuiya-ke'

@bot.route('/', methods=['GET'])
def verification():
  if request.args.get('hub.verify_token', '') == VerifyToken:
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'


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