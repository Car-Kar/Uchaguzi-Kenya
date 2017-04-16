from flask import Flask, request
import json
import requests
import tokens

app = Flask(__name__)

PAT = tokens.PAT
VerifyToken = tokens.token

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
  messages = request.get_json
  for message in messages['entry']:
  	for msg in message['messaging']:
  		SenderID = msg['sender']['id']
  		MessageText = msg['message']['text']
  		RecipientID = msg['recipient']['id']
  		if msg.get('message'):
  			if MessageText.lower() == 'hi' or MessageText.lower() = 'Hello':
  				SendMessage(SenderID, HelloMessage)

  return 'ok', 200


def SendMessage(VerifyToken, RecipientID, Text):
  """Send the message text to recipient with id recipient.
  """

  parameters = {
  	'access-token' : 'VerifyToken'
  }
  headers = {
  	'Content-Type' : 'application/json'
  }
  data = json.dumps({
  	'recipient': {
  		'id': 'RecipientID'
  	},
  	'message' : {
  		'text': 'message_text'
  	}
  	})
  r = requests.post('https://graph.facebook.com/v2.6/me/messages', params = parameters, headers = headers, data = data)

if __name__ == '__main__':
  app.run(debug = True)