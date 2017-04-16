from flask import Flask, request
import json
import requests

app = Flask(__name__)

PAT = 'EAAENedDtJT4BAEgVkRvp8gKskLKdi2VjGIXj30o6LNUuK3i07be220JnOfxIyeqB5B9Xag1AhaR4kHEgXyf5TOHSvOymLps6xOT77Da139Gemt3OixtonTLLWlfnx2azuULens9o0Cgx1QhZCCAmWYZAHYsZBZAzWEbT9JP8OAZDZD'
VerifyToken = 'test-token'

HelloMessage = """
Hello!
My name is ElectionBot, and I provide you with information about the 2017 National Elections candidates.
"""


@app.route('/', methods=['GET'])
def verification():
  if request.args.get('hub.verify_token', '') == VerifyToken:
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def GetMessages():
  messages = request.get_json()
  if messages['object'] == 'page':
    for message in messages['entry']:
        for msg in message['messaging']:
            SenderID = msg['sender']['id']
            MessageText = msg['message']['text']
            RecipientID = msg['recipient']['id']
            if msg.get('message'):
                if MessageText.lower() == 'hi' or MessageText.lower() == 'hello':
                    SendMessage(SenderID, 'KK')

  return 'ok', 200


def SendMessage(RecipientID, Text):
    print('Sending message')
    ''' parameters = {
    'access-token' : AccessToken
    }'''
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient': {
        'id': 'RecipientID'
    },
    'message' : {
        'text': Text
    }
    })
    r = requests.post('https://graph.facebook.com/v2.8/me/messages/?access_token' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def Name(name):
    name = name.split()
    name = '-'.join(name)
    return name.lower()

if __name__ == '__main__':
  app.run(debug = True)
