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
                if MessageText.lower() == 'hi' or MessageText.lower() == 'hello' or MessageText.lower == 'hey':
                    SendMessage(SenderID, HelloMessage)
                    CampaignMenu(SenderID)


  return 'ok', 200


'''def GreetingText(RecipientID):
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'setting-type' : 'greeting',
        'greeting' : {
        'text' : 'Hi!'
        }

        }
        )
    r = requests.post('https://graph.facebook.com/v2.8/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    
'''

def SendMessage(RecipientID, Text):
    print(('Sending message to {0}').format(RecipientID))

    ''' parameters = {
    'access-token' : AccessToken
    }'''
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient': {
        'id': RecipientID
    },
    'message' : {
        'text': Text
    }
    })
    r = requests.post('https://graph.facebook.com/v2.8/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def CampaignMenu(RecipientID):
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient' : {
            'id' : RecipientID
        },
        'message' : {
            'attachment' : {
                'type' : 'template',
                'payload' : {
                    'template_type' : 'button',
                    'text' : 'What election level do you want to know more about?',
                    'buttons' : [
                        {
                            'type' : 'postback',
                            'title' : 'Presidential Elections',
                            "payload":"USER_DEFINED_PAYLOAD"
                        },
                        {
                            'type' : 'postback',
                            'title' : 'Governor Elections',
                            "payload":"USER_DEFINED_PAYLOAD"
                        },
                        {
                            'type' : 'postback',
                            'title' : 'Woman Representative',
                            "payload":"USER_DEFINED_PAYLOAD"
                        }

                    ]

                }
            }
        }

        }
        )
    r = requests.post('https://graph.facebook.com/v2.8/me/messages/?access_token=' + PAT,  headers=headers, data=data)


def Name(name):
    name = name.split()
    name = '-'.join(name)
    return name.lower()

if __name__ == '__main__':
  app.run(debug = True)
