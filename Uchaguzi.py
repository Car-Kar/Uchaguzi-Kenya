from flask import Flask, request
import json
import requests
import pymongo
from pymongo import MongoClient
from wit import Wit


app = Flask(__name__)


PAT = 'EAAarLkMVMy4BALcfghCBksMQuo5lqLMIsogY1OJEHxVDJZAdIR0KkKWqfdCEbbRIv7IeFrsTTEAFfNRo3y0vgFmZA7wCkcYsZAQSEwlBL6V5VZAexpR4LO4IB1hZAhaoDYejvT5hLjCeZCaiye8qCa5vNrOOGuSyAuWE5ZCZB5VMfwZDZD'
VerifyToken = '0454'
WitToken = 'DYIOAENA3VUYMZ2QHFQ6OX3AOZ3P3D3V'
client = Wit(access_token = WitToken)

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
VoterRequirements = '''
The national elections are on Tuesday, August 8th.
You will need to have registered as a voter and carry your national identification, or passport to vote.
Please come out in support for our best future leaders.
'''
KiswahiliRequirements = '''Uchaguzi wa kitaifa uko siku ya Jumanne, August 8.
Unahitaji kuwa umesajiliwa kama mpiga kura na kuwa na kitambulisho chako cha kitaifa, au pasipoti ya kupiga kura.
Tafadhali kuja  kwa ajili ya kuchagua viongozi wetu bora ya baadaye.'''


CandidateMoreInfo = '''Do you want to know more about one of these candidates?

If so, send me his or her name.

'''
CountiesMessage = ''''
We are only supporting three counties right now; Kisumu, Mombasa and Nairobi.
Please check back from time to time as we integrate more counties!
\U0001F642
'''
ApologyMessage = '''
Sorry, I didn't get that.
Would you mind repeating it?
'''

Counties = ['kiambu', 'kisumu', 'mombasa', 'nairobi', 'nakuru']
OtherCounties = ''' Thank you for using Uchaguzi.
However, this is our first beta and us such we can only provide information for Kiambu, Kisumu, Mombasa, Nairobi, or Nakuru.
Please use any of those five counties for now, as we go about adding information support for all other counties!
\U0001F642
'''
ContinueUsing = '''You can always choose another option to continue using me after you're done with one option, or you can say goodbye if you're done!
\U0001F642
'''
Goodbye = '''
Thank you for the time! 
I hope you have learnt enough about our candidates to make an informative decision come August!
Goodbye!
\U0001F642
'''

LanguageText = ''''What Language do you want to continue with?
Choose one from the options below.'''

ResponseStack = []
KiswahiliHello = 'Jambo! '
Options = ['governor', 'senator', 'women representative', 'members of parliament']
Kiswahili = False
uri = 'mongodb://MC:se*8DGs6t8F*39*k@ds149491.mlab.com:49491/uchaguzike'


class UsingMongo:
    def __init__(self):
        self.DB = ''

    def MongoConnection(self, uri):
        try:
            client = MongoClient(uri)
            self.DB = client.get_default_database()
            self.DB.authenticate('MC', 'se*8DGs6t8F*39*k')
            print('Connection Successful!')
            return self.DB
        
        except Exception as e:
            raise e
            print('Connection Unsuccessful!')

    def IncomingKiswahiliUsers(self, FromUser, data):
        collection = self.DB['kiswahili']
        print('Connected to kiswahili users collection!')
        user =  collection.find_one({'fromuser': FromUser})
        if user is not None:
            swahili = True
            return swahili
        else:
            if 'kiswahili' == data.lower():
                language = collection.insert({'fromuser': FromUser})
                print('Added new Kiswahili User!')
                return True

MDB = UsingMongo()


@app.route('/', methods=['GET'])
def verification():
  if request.args.get('hub.verify_token', '') == VerifyToken:
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def StartMessaging():
    try:
        db = MDB.MongoConnection(uri)
        messages = request.get_json()
        if messages['object'] == 'page':
            for message in messages['entry']:
                for msg in message['messaging']:
                    SenderID = msg['sender']['id']
                    MessageText =msg['message']['text']
                    entity, value = UsingWit(MessageText)
                    #QuickReply = msg['quick_reply']['payload']
                    Kiswahili = MDB.IncomingKiswahiliUsers(SenderID, MessageText)
                    if msg.get('message'):
                        if 'start' in MessageText.lower():
                            SendMessage(SenderID, LanguageText)
                        if Kiswahili == True:
                            SendMessage(SenderID, 'Fucker.')
                        if entity == 'names':
                            response = 'Hello' + str(value)
                            SendMessage(SenderID, response)
                       

                    elif msg.get('postback'):
                        PostbackText = msg['postback']['payload']
                        Kiswahili = MDB.IncomingKiswahiliUsers(SenderID, PostbackText)
                        if Kiswahili == True and PostbackText == 'VoterReq':
                            SendMessage(SenderID, VoterRequirements)
    except Exception as e:
        raise e

    return 'OK', 200



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
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def send(request, response):
    fb_id = request['session_id']
    text = response['text']
    SendMessage(SenderID, text)


def UsingWit(TEXT):
    response = client.message(TEXT)
    entity = None
    value = None

    try:
        entity = list(response['entities'])[0]
        value = response['entities'][entity][0]['value']
    except:
        pass

    return (entity, value)





if __name__ == '__main__':
    app.run(debug = True)