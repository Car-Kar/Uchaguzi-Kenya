from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

PAT = 'EAAENedDtJT4BAEgVkRvp8gKskLKdi2VjGIXj30o6LNUuK3i07be220JnOfxIyeqB5B9Xag1AhaR4kHEgXyf5TOHSvOymLps6xOT77Da139Gemt3OixtonTLLWlfnx2azuULens9o0Cgx1QhZCCAmWYZAHYsZBZAzWEbT9JP8OAZDZD'
VerifyToken = 'test-token'

HelloMessage = """
Hello!
My name is Uchaguzi, and I provide you with voter and candidate information for the 2017 National Elections.
"""
MoreInfo = '''
Which candidate do you want to know more about?

(Send me his or her name.)

'''

BaseUrl = 'http://myaspirantmyleader.co.ke/'


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
            if msg.get('message'):
                MessageText = msg['message']['text']
                if MessageText.lower() == 'hi' or MessageText.lower() == 'hello' or MessageText.lower == 'hey':
                    SendMessage(SenderID, HelloMessage)
                    CampaignMenu(SenderID)
                if 'moses' in MessageText.lower():
                    y = 'Moses Masika Wetangula'
                    a = CandidateInfo(y)
                    SendMessage(SenderID, a)


            if msg.get('postback'):
                PostbackText = msg['postback']['payload']
                if PostbackText == 'Presidential Elections':
                    names = Candidates()
                    SendMessage(SenderID, names)
                    SendMessage(SenderID, MoreInfo)



  return 'ok', 200

'''@app.route('/', methods=['POST'])
def GetStarted():
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'setting_type': 'call_to_actions',
        'thread_state' : 'new_thread',
        'call_to_actions' : [
        {
             'payload' : 'Get Started'
    }]
})
    r = requests.post('https://graph.facebook.com/v2.8/me/thread_settings?access_token=' + PAT,  headers=headers, data=data)
    
@app.route('/', methods=['POST'])
def GreetingText():
    header = {
    'Content-type' : 'application/json'
    }
    data = json.dumps({
        'greeting' : [
        {
        'locale' : 'default',
        'text' : HelloMessage
        }]
        })
    r = requests.post('https://graph.facebook.com/v2.8/me/messenger_profile?access_token=' + PAT,  headers=headers, data=data)

def MainMenu():
    headers = {
    'Content-Type' : 'application/json'
    }

    data = json.dumps({

        })'''

def SendMessage(RecipientID, Text):
    print(('Sending message to {0}').format(RecipientID))

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
                            'payload': 'Presidential Elections'
                        },
                        {
                            'type' : 'postback',
                            'title' : 'Governor Elections',
                            'payload':"USER_DEFINED_PAYLOAD"
                        },
                        {
                            'type' : 'postback',
                            'title' : 'Woman Representative',
                            'payload':"USER_DEFINED_PAYLOAD"
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

def Candidates():
    Url = BaseUrl + 'members/presidential-candidates/'
    RQT = requests.get(Url)
    DATA = RQT.text
    SD = BeautifulSoup(DATA, 'html.parser')
    for match in SD.find_all('div', class_ = 'col-md-3 col-sm-6 col-xs-12'):
        NT = match.find('h3')
        name = NT and ''.join(NT.stripped_strings)
    return name
        

def CandidateInfo(name):
    z = Name(name)
    Url = BaseUrl + 'member/' + z + '/'
    RQT2 = requests.get(Url)
    DATA2 = RQT2.text
    SD2 = BeautifulSoup(DATA2, 'html.parser')
    for match in SD2.find_all('div', class_='member-content'):
        info_tag = match.find('p')
        info = info_tag and ' '.join(info_tag.stripped_strings)
        return info


if __name__ == '__main__':
  app.run(debug = True)
