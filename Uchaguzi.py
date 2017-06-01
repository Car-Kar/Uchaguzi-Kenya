from flask import Flask, request
import json
import requests
import pymongo
from pymongo import MongoClient
from wit import Wit


app = Flask(__name__)


PAT = 'EAAarLkMVMy4BAERvNFAqZBaIfdpnrILzYWnLXeUhst52bj6d6oiA3YewwP7UvhDDGHdWciSElZCtZAWNnN15IbCZB10kepGG0BbkwAErwzi3jWnPZA6tPSh985a2j38lcrhRTNFFNaWZAvy6qv2FejYK7ZCaqgSXZCKm5D9V0vsj0QZDZD'
VerifyToken = '0454'
WitToken = 'DYIOAENA3VUYMZ2QHFQ6OX3AOZ3P3D3V'
client = Wit(access_token = WitToken)

SurveyUrl = 'https://m.me/672849446250204/?ref=f258b3c90e014ce15030df0a91a0a322'

Start = '''Hello There!
What language do you want to continue in?
'''

IntroductoryMessage = ''' The 2017 Kenyan National Elections are taking place in August.
I am a tool for you to acquire more information on voting and the vying candidates.
I have a top-level menu which you can access at any time by pressing the menu icon (\u2630)  at the bottom to choose the option that you want.
Go ahead, try it.
\U0001F642
'''
IntroductoryMessage2 = '''I provide information on voting procedures, voter registration, your county administration, the vying candidates, and government .'''
KiswahiliIntroduction2 = '''Nitakupa taarifa kuhusu taratibu kupiga kura, usajili wa wapiga kura, utawala wa kata yako, wagombea wanaogombea na ukaguzi wa serikali.'''
KiswahiliIntroduction = '''Jambo!
Uchaguzi wa Taifa wa Kenya unafanyika Agosti.
Mimi ni chombo kwa ajili ya wewe kupata taarifa zaidi juu ya kupiga kura na wagombea wanaogombea.
Nina orodha ambayo unaweza kupata wakati wowote kwa kubonyeza menu (\u2630) hapo chini ili kuchagua chaguo unataka.
\U0001F642'''
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
OptionsText = 'Choose an option below to continue.'
KiswahiliOptions = 'Chagua chaguo kuendelea.'

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
        if user is not None and 'english' == data.lower():
            print('Changed a language!')
            language = collection.delete_one({'fromuser': FromUser})
            swahili = False
            return swahili
        elif user is not None:
            swahili = True
            return swahili
        else:
            if 'kiswahili' == data.lower():
                language = collection.insert({'fromuser': FromUser})
                print('Added new Kiswahili User!')
                swahili = True
                return swahili
            elif 'english' == data.lower():
                swahili = False
                return swahili

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
        print(messages)
        if messages['object'] == 'page':
            for message in messages['entry']:
                for msg in message['messaging']:
                    print(msg)
                    SenderID = msg['sender']['id']
                    #entity, value = UsingWit(MessageText)
                    #FindingUser(SenderID)
                    response = None
                    #UserSays = ReturnType(msg)
                    surveying = False
                    #Kiswahili = MDB.IncomingKiswahiliUsers(SenderID, UserSays)
                    if msg.get('message'):
                        MessageText = msg['message']['text']
                        if 'start' in MessageText.lower():
                            SendMessage(SenderID, Start)
                            #ReusableOptions(SenderID, Start, 'Kiswahili', 'English')


                        
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




if __name__ == '__main__':
    app.run(debug = True)