from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

PAT = 'EAAENedDtJT4BAEgVkRvp8gKskLKdi2VjGIXj30o6LNUuK3i07be220JnOfxIyeqB5B9Xag1AhaR4kHEgXyf5TOHSvOymLps6xOT77Da139Gemt3OixtonTLLWlfnx2azuULens9o0Cgx1QhZCCAmWYZAHYsZBZAzWEbT9JP8OAZDZD'
VerifyToken = 'test-token'

IntroductoryMessage = ''' The 2017 Kenyan National Elections are taking place in August.
I am a tool for you to acquire more information on voting and the vying candidates.
I have a top-level menu which you can access at any time by pressing the menu icon (\u2630)  at the bottom to choose the option that you want.
Go ahead, try it.
\U0001F642
'''
VoterRegistration = '''Thank you for using Uchaguzi!
However due to logistical circumstances, the option of finding out your registration status is not available right now.
Please check again in a little while as we go about incorporating it.
'''
CandidateMoreInfo = '''
Which candidate do you want to know more about?

(Send me his or her name.)

'''


BaseUrl = 'http://myaspirantmyleader.co.ke/'
candidates = []


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
                if 'president' in MessageText.lower():
                    names = Candidates()
                    TEXT = 'The presidential candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)

                if 'moses' in MessageText.lower():
                    y = 'Moses Masika Wetangula'
                    a = CandidateInfo(y)
                    SendMessage(SenderID, a)


            if msg.get('postback'):
                PostbackText = msg['postback']['payload']
                if PostbackText == 'Get Started':
                    SendMessage(SenderID, IntroductoryMessage)
                elif PostbackText == 'presidential':
                    names = Candidates()
                    TEXT = 'The' + PostbackText + 'candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)

                elif PostbackText == 'gubernatorial' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT1)
                    TEXT2 = 'The' + PostbackText + 'candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'senate' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT1)
                    TEXT2 = 'The' + PostbackText + 'candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'womrep' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT1)
                    TEXT2 = 'The candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'parliamentary' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT1)
                    TEXT2 = 'The' + PostbackText + 'candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'VoterReg':
                    SendMessage(SenderID, VoterRegistration)




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



'''def CampaignMenu(RecipientID):
    print("Sending menu")
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
                            'payload': 'Presidential'
                        },
                        {
                            'type' : 'postback',
                            'title' : 'Governor Elections',
                            'payload':"governors"
                        },
                        {
                            'type' : 'postback',
                            'title' : 'Senator Elections',
                            'payload' : 'senators'
                        },
                        {
                            'type' : 'postback',
                            'title' : 'Woman Representative',
                            'payload':"wom-rep"
                        },
                        {
                            'type' : 'postback',
                            'title': 'Members of Parliament',
                            'payload' : 'mp'

                        }

                    ]

                }
            }
        }

        }
        )
    r = requests.post('https://graph.facebook.com/v2.8/me/messages?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)
'''

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
        PT = match.find('span')
        party = PT and ''.join(PT.stripped_strings)
        candidates.append([name, party])
    return candidates
        

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
