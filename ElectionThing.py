from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup
import urllib


app = Flask(__name__)

PAT = 'EAAa9qNLjjJwBAFog5Pj5n67hTsQwS6Ieqr1eCaBEkg4MvqDfV4M6AgowkSFhSKGavs4tmGCOt3tZCnOajxFdXben0sCMf6AzcCjf23rDDqsPW4OKuRXKg9i6qbMUzaZBJfcCvT4RfZCIwZB4uNkbofiATWO3uijTZAE95cLshLQZDZD'
VerifyToken = '0454'

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
LanguageText = ''' In what language do you want to continue in?
You can choose by clicking one of the buttons, or by just sending your language choice between the two to me.
'''
SChoice = ''' Jambo!
Chagua aina ya uchaguzi unaoutaka kutoka kwa orodha hapo chini.
'''

ApologyMessage = '''
Sorry, I didn't get that.
Would you mind repeating it?
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
                elif  MessageText.lower() == 'moses':
                    y = 'Moses Masika Wetangula'
                    a = CandidateInfo(y)
                    SendMessage(SenderID, a)
                elif MessageText.lower() == 'kiambu':
                    names = Search(MessageText, 'governor')
                    ST = 'The candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, ST)
                else:
                    SendMessage(SenderID, ApologyMessage)


            elif msg.get('postback'):
                PostbackText = msg['postback']['payload']
                if PostbackText == 'Get Started':
                    LanguageMenu(SenderID)
                elif PostbackText == 'english':
                    SendMessage(SenderID, IntroductoryMessage)
                
                        #SendMessage(SenderID, IntroductoryMessage)
                '''elif PostbackText == 'presidential':
                    names = Candidates()
                    TEXT = 'The presidential candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                elif PostbackText == 'gubernatorial':
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'senate' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT2)
                    TEXT2 = 'The' + PostbackText + 'candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'womrep' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT2)
                    TEXT2 = 'The candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'parliamentary' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT2)
                    TEXT2 = 'The' + PostbackText + 'candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'VoterReg':
                    SendMessage(SenderID, VoterRegistration)'''




  return 'ok', 200

   

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

def LanguageMenu(RecipientID):
    print("Sending options for language")
    headers = {
    'Content-type' : 'application/json'
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
                    'text' : LanguageText,
                    'buttons' : [
                    {
                        'type' : 'postback',
                        'title' :  'English',
                        'payload' : 'english'
                    },
                    {
                        'type' : 'postback',
                        'title' : 'Kiswahili',
                        'payload' : 'kiswahili' 
                    }]
                }

        }
        }
        })
    RT = requests.post('https://graph.facebook.com/v2.8/me/messages?access_token=' + PAT,  headers=headers, data=data)
    if RT.status_code != 200:
        print(RT.text)

def Kiswahili(SID):
    SendMessage(SID, SChoice)
    messages = requests.get_json()
    if messages['object'] == 'page':
        for message in messages['entry']:
            for msg in message['messaging']:
                SID = msg['sender']['id']
                if msg.get('postback'):
                    PT = msg['postback']['payload']
                    if PT == 'presidential':
                        names = Candidates()
                        TXT = 'Wagombea wa urais ni: \n' + str(names[0:])
                        SendMessage(SID, TXT) 
                    elif PT == 'gubernatorial':
                        pass
                    elif PT == 'senate':
                        pass
                    elif PT == 'womrep':
                        pass
                    elif PT == 'parliamentary':
                        PT



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
        fmt = '{0} - {1}.'.format(name, party)
        candidates.append(fmt)
    candidate = '\n'.join([str(cand) for cand in candidates])
    return candidate
        

def CandidateInfo(name):
    print('Getting info')
    z = Name(name)
    Url = BaseUrl + 'member/' + z + '/'
    RQT2 = requests.get(Url)
    DATA2 = RQT2.text
    SD2 = BeautifulSoup(DATA2, 'html.parser')
    for match in SD2.find_all('div', class_='member-content'):
        info_tag = match.find('p')
        info = info_tag and ' '.join(info_tag.stripped_strings)
        return info

def Search(CountyName, Level):
    CountyName = CountyName.title() + '+County'
    parameters = {
    "upme_search[county]" : CountyName,
    "upme-search"  :  "Search+&+Filter"
    }
    search = BaseUrl  + 'candidates/' + Level + '-candidates/'
    ToSearch = requests.post(search, params=parameters)
    y = ToSearch.status_code
    if y == 200:
        TS = ToSearch.text
        TS = BeautifulSoup(TS, 'html.parser')
        for match in TS.find_all('div', class_= 'upme-team-design-three upme-team-design'):
            for tags in match.find('div', class_ = 'upme-author-name'):
                name_tag = tags.find('a')
                name = name_tag.string
                return name


if __name__ == '__main__':
  app.run(debug = True)


#counties - Nairobi, Kiambu, Nakury, Mombasa, Kisumu