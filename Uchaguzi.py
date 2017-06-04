from flask import Flask, request
import json
import requests
import pymongo
from pymongo import MongoClient
from wit import Wit
import datetime
from datetime import date
import os
import sys
from datetime import date
#from apscheduler.scheduler import Scheduler
import re
import pymysql
import sys

app = Flask(__name__)


#sched = Scheduler()


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

Counties = ['kiambu', 'kisumu', 'mombasa', 'nairobi', 'nakuru', 'kakamega', 'kiambu', 'uasin gishu', 'turkana', 'narok', 'kericho']
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


    def Subscribers(self, FromUser,  data):
        collection = self.DB['reminders']
        user =  collection.find_one({'fromuser': FromUser})
        if user is not None: 
            time =  user['time']
            return time
        else:
            if 'week' in data.lower():
                time = collection.insert_one({'fromuser' : FromUser}, {'time': 'week'})
                return time
            elif 'day' in data.lower():
                time = collection.insert_one({'fromuser' : FromUser}, {'time': 'day'})
                return time


    def PresidentialRace(self, pres):
        collection = self.DB['presidentialrace']
        print('Connected to presidents collection!')
        regex = re.compile('.*(%s).*'%pres)
        user =  collection.find_one({'name': {'$regex' : '^regex'}})
        if user is not None:
            votes = user['votes']
            collection.update_one({'name' : pres}, {'$set': {'votes': votes + 1}})
            print(votes)
        else:
            pass

class UsingSQL:
    def __init__(self):
        self.DB = ''

    def SQLConnection(self):
        try:
            conn = pymysql.connect(user='b5ad6687738858',passwd='23bfecef',host = 'us-cdbr-iron-east-03.cleardb.net', database='heroku_611862edb2b2330')
            self.curs = conn.cursor()
            print("Connection to database successful!")
            return self.curs
        
        except Exception as e:
            raise e
            print('Connection Unsuccessful!')

    def all_presidential_candidates(self):
        self.curs.execute("""SELECT name, political_party FROM presidential_candidates""")
        results = list(self.curs.fetchall())
        result = '\n'.join([str(cand) for cand in results])
        result = result.replace('(', ' ')
        result = result.replace(')', ' ')
        result = result.replace("'", ' ')
        result = result.replace(',', '-')
        print(result)
        return result

    def all_presidential_names(self):
        self.curs.execute("""SELECT name FROM presidential_candidates""")
        results = self.curs.fetchall()
        candidates = []
        for row in results:
            candidates.append(row[0])
        return candidates

    def president_bio(self, value):
        self.curs.execute("""SELECT running_mate,political_bio FROM presidential_candidates WHERE UPPER(name) Like  UPPER('%s') """ % (value))
        result = self.curs.fetchall()
        mate = []
        bio = []
        for row in result:
            return row[0], row[1]

    def governor_bio(value):
        self.curs.execute("""SELECT running_mate,political_bio FROM governor_candidates WHERE UPPER(name) Like  UPPER('%s') """ % (value))
        result= self.curs.fetchall()
        #print(str(result))
        return result

    def governors(value):
        self.curs.execute("""SELECT name, political_party FROM governor_candidates WHERE UPPER(county) Like  UPPER('%s') """ % (value))
        results = list(self.curs.fetchall())
        result = '\n'.join([str(cand) for cand in results])
        result = result.replace('(', ' ')
        result = result.replace(')', ' ')
        result = result.replace("'", ' ')
        result = result.replace(',', '-')
        print(result)
        return result






MDB = UsingMongo()
SQL = UsingSQL()

options = ['gov', 'sen', 'wom']
VotingInformation = {'image' : 'https://media.giphy.com/media/3o6ZtkFObzcJiaMOFG/giphy.gif', 'image' : 'https://media.giphy.com/media/26vUCOMzBiBZ0qW1a/giphy.gif', 
'video' : 'https://www.youtube.com/watch?v=nQbztjkag1A&feature=youtu.be&t=1',  'image' : 'https://farm5.staticflickr.com/4267/34872767952_f36c5a4dda_o_d.jpg'}

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
        InfoDB = SQL.SQLConnection()
        db = MDB.MongoConnection(uri)
        messages = request.get_json()
        print(messages)
        if messages['object'] == 'page':
            for message in messages['entry']:
                for msg in message['messaging']:
                    print(msg)
                    SenderID = msg['sender']['id']
                    FindingUser(SenderID)
                    response = None
                    UserSays = ReturnType(msg)
                    value = UsingWit(UserSays)
                    surveying = False
                    Kiswahili = MDB.IncomingKiswahiliUsers(SenderID, UserSays)
                    cands = FindingCandidate(UserSays)
                    print(cands)
                    #News = MDB.NewsSubscribers(SenderID, UserSays)
                    #print(Kiswahili)
                    level = Level(UserSays)
                    print(level)
                    race = MDB.PresidentialRace(UserSays)
                    cs = SQL.all_presidential_names()
                    if msg.get('message'):
                        #matching = [s for s in cs if str(ResponseStack.pop()) in s]
                        #print(matching)
                        if 'start' in UserSays.lower() or 'hey' in UserSays.lower() or 'hi' in UserSays.lower() or 'hello' in UserSays.lower():
                            ReusableOptions(SenderID, Start, 'Kiswahili', 'English')
                        if Kiswahili == True and 'swahili' in UserSays.lower():
                            SendMessage(SenderID, KiswahiliIntroduction)
                            SendMessage(SenderID, KiswahiliIntroduction2)
                            GenericTemplateOptions(SenderID, 
                                'Kupiga Kura', 'Tunakupa mawaidha kuhusu kupiga kura', 'Wagombea', 'Jua nani anagombea cheo cha serikali', 'Serikali', 'Pata ujumbe kuhusu serikali ya kata yako.',
                                'Mahitaji ya Kura', 'Weka Mawaidha',
                                'Chagua cheo cha kura',
                                'Kagua Serikali',
                                'Wasiliana na serikali ya kata yako')
                        if Kiswahili is not True and 'english' in UserSays.lower():
                            SendMessage(SenderID, IntroductoryMessage)
                            SendMessage(SenderID, IntroductoryMessage2)
                            GenericTemplateOptions(SenderID)

                        if Kiswahili == True and 'nipe' in UserSays.lower():
                            SendMessage(SenderID, VoterRequirements)
                        '''if Kiswahili == True and UserSays == oi:
                            response = 'Naweza kupa ujumbe kuhusu kupiga kura, au kuweka mawaidha ya kukukumbusha kupiga kura.'
                            SendMessage(SenderID, response)
                            ReusableOptions(SenderID, KiswahiliOptions, 'Nipe Ujumbe', 'Mawaidha')'''
                        if Kiswahili == True and 'mawaidha' in UserSays.lower():
                            response = '''Nitakutumia alani ya kukukumbusha siku ya uchaguzi.
                            Unataka alani ya siku gani?'''
                            ReusableOptions(SenderID, response, 'A Week Before', 'Two Days Before')

                        if Kiswahili is not True and 'vote for' in UserSays.lower():
                            response = 'What presidential candidate would you vote for if the elections were tomorrow?'
                            SendMessage(SendMessage, response)
                        if Kiswahili is not True and 'see results' in UserSays.lower():
                            WebView(SenderID, 'https://uchaguzi.herokuapp.com/')

                        if Kiswahili is not True and 'a week' in UserSays.lower():
                            response = 'I will be messaging you a week before the elections as a reminder'
                            SendMessage(SenderID, response)

                        if Kiswahili is not True and 'two days' in UserSays.lower():
                            response = 'I will be messaging you two days before the elections as a reminder'
                            SendMessage(SenderID, response)
                            Home(SenderID, 'Go back to home?', 'Home')

                        if Kiswahili is not True and UserSays.lower() in options:
                            response = 'You have successful subscribed! I will be messaging you weekly to give you up to date news!'
                            SendMessage(SenderID, response)
                            Home(SenderID, 'Go back to home?', 'Home')

                        if Kiswahili is not True and 'home' in UserSays.lower():
                            GenericTemplateOptions(SenderID)

                        if 'from what' in UserSays.lower():
                            print('Fuck you facebook')
            

                        elif 'evans' in UserSays.lower() or 'kidero' in UserSays.lower():
                            SendMessage(SenderID, g_evans_info)
                            SendMessage(SenderID, ContinueUsing)
                            Home(SenderID, 'Go back to home?', 'Home')
                    
                        elif 'mike' in UserSays.lower() or 'sonko' in UserSays.lower():
                            SendMessage(SenderID, g_mike_info)
                            SendMessage(SenderID, ContinueUsing)
                            Home(SenderID, 'Go back to home?', 'Home')

                        

                        elif 'bye' in UserSays.lower():
                            SendMessage(SenderID, Goodbye)

                        elif UserSays.lower() in cands.lower():
                            print('Yes')
                            query = '%' + UserSays.lower() + '%'
                            run, bio = SQL.president_bio(query)
                            running_mate = 'His running mate is ' + str(run)
                            bio = str(bio)
                            SendMessage(SenderID, running_mate)
                            if len(bio) > 640:
                                bio, bios = CheckTextLength(bio)
                                response = bio + '-'
                                SendMessage(SenderID, response)
                                SendMessage(SenderID, bios)
                            else:
                                SendMessage(SenderID, bio) 

                        elif lvl is not None and 'gov' == lvl.lower() and 'nairobi' in UserSays.lower():
                            query = '%nairobi%'
                            candidates = SQL.governors(query)
                            response = 'The gubernatorial candidates are: \n' + str(candidates[0:])
                            SendMessage(SenderID, response)


                            


                    
                        

                    elif msg.get('postback'):  
                        if UserSays == 'Get Started':
                            ReusableOptions(SenderID, Start, 'Kiswahili', 'English')

                        if Kiswahili == True and UserSays == 'survey':
                            TakeSurvey(SenderID, 'Tafadhali Jibu maswali haya ili - review them.', SurveyUrl, 'SurveyName')
                        ''''elif Kiswahili is not True and UserSays == 'subscribe':
                            response = 'What level of election do you want to get weekly news for?'
                            UsingOptions(SenderID, response, 'Presidential', 'Governor', 'Senate', 'Women Representative')
'''
                        if Kiswahili == False and UserSays == 'survey':
                            TakeSurvey(SenderID, 'Please take the following survey to review your county administration', SurveyUrl, 'SurveyName')

                        if Kiswahili is not True and UserSays == 'levels':
                            LevelTemplateOptions(SenderID,
                                'Presidential Candidates.',
                                'Know the vying presidential candidates and their running mates.',
                                'Governor Candidates.',
                                'Know the vying gubernatorial candidates and their running mates.',
                                'Senator Candidates.',
                                'Know the vying senate candidates and their running mates.',
                                'Women Representatives Candidates.',
                                'Know the vying candidates and their policies.',
                                'Presidential Candidates',
                                'Take the presidential poll',
                                'Governors Candidates',
                                'Senator Candidates',
                                'Women Representative Candidates'
                                )
                        if Kiswahili is not True and UserSays == 'voters':
                            SendMessage(SenderID, VoterRequirements )
                            SendMessage(SenderID, 'Here are some helpful graphics to help you.')
                            
                            SendAttachment(SenderID,'image', 'https://farm5.staticflickr.com/4248/34872766342_a66c0fa485_o_d.jpg')
                            SendMessage(SenderID, ContinueUsing)
                            Home(SenderID, 'Go back to home?', 'Home')

                        elif Kiswahili is not True and UserSays == 'poll':
                            ReusableOptions(SenderID, OptionsText, 'Vote for your preferred candidate', 'See the results.')

                        elif Kiswahili is not True and UserSays == 'registration':
                            SendAttachment(SenderID, 'image', 'https://farm5.staticflickr.com/4243/34193089344_55a2249bd6_o_d.jpg')
                            SendMessage(SenderID, VoterRegistration)
                            Home(SenderID, 'Go back to home?', 'Home')

                        elif Kiswahili is not True and UserSays == 'gov':
                            SendMessage(SenderID, 'From what county?')

                        elif Kiswahili is not True and 'subscribe' in UserSays:
                            WebView(SenderID, 'News', 'http://www.nation.co.ke/page/search/DailyNation/election2017/3439870-3439870-view-asSearch-ccr8qt/index.html', 'The Top Election News Today')
                            


                        elif Kiswahili is not True and UserSays == 'reminder':
                            ReusableOptions(SenderID, 'When would you like to get a reminder notification for the elections?', 'A Week Before', 'Two Days Before')


                        elif Kiswahili is not True and UserSays == 'pres':
                            candidates = SQL.all_presidential_candidates()
                            print(candidates)
                            first_names, second_names = CheckListLength(candidates)
                            response = 'The presidential candidates are: \n' + str(first_names[0:])
                            SendMessage(SenderID, response)
                            SendMessage(SenderID, second_names)
                            SendMessage(SenderID, CandidateMoreInfo)

                        








                        
    except Exception as e:
        raise e

    return 'OK', 200


''''@app.route('/', methods=['POST'])
def Subscribed(SenderID, week, day):
    try:
        db = MDB.MongoConnection(uri)
        messages = request.get_json()
        print(messages)
        if messages['object'] == 'page':
            for message in messages['entry']:
                for msg in message['messaging']:
                    SenderID = msg['sender']['id']
                    if msg.get('message'):
                        MessageText = msg['message']['text']
                        su = MDB.Subscribers(SenderID, MessageText)
                        if week == True:
                            response = The national elections are coming up in week! 
                                    Please remember to show up and vote for your leaders!
                                \U0001F44D

                            SendMessage(su, response)

                        elif day == True:
                            response = The national elections are coming up in two days time! 
                            Please remember to show up and vote for your leaders!
                            \U0001F44D

                            SendMessage(su, response)


    except Exception as e:
        raise e

    return 'OK', 200'''


def ReturnType(msg):
    print('Checking Type')
    if msg.get('message'):
        MessageText = msg['message']['text']
        return MessageText
    elif msg.get('postback'):
        PostbackText = msg['postback']['payload']
        return PostbackText
    elif msg.get('web_url'):
        URLText = msg['web_url']['title']
        return URLText

def FindingCandidate(name):
    candidates = SQL.all_presidential_names()
    result = [c for c in candidates if name.lower() in c.lower()]
    result = ' '.join(result)
    return result.lower()

def Home(RecipientID, TXT, op1):
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient': {
        'id': RecipientID
    },
    'message' : {
        'text': TXT,
        'quick_replies':[
      {
        'content_type': 'text',
        'title' : op1,
        'payload' : 'IsReusable'
      }
    ]
    }
    })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def ReusableOptions(RecipientID, Text, op1, op2):
    print(('Sending message to {0}').format(RecipientID))

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient': {
        'id': RecipientID
    },
    'message' : {
        'text': Text,
        'quick_replies':[
      {
        'content_type': 'text',
        'title' : op1,
        'payload' : 'IsReusable'
      },
      {
        'content_type' : 'text',
        'title' : op2,
        'payload': 'IsReusable'
      }
    ]
    }
    })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def UsingOptions(RecipientID, Text, O1, O2, O3, O4):
    print(('Sending message to {0}').format(RecipientID))

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient': {
        'id': RecipientID
    },
    'message' : {
        'text': Text,
        'quick_replies':[
      {
        'content_type' : 'text',
        'title' : O1,
        'payload' : 'pres'
      },
      {
        'content_type' : 'text',
        'title' : O2,
        'payload' : 'gov'
      },
      {
        'content_type' : 'text',
        'title' : O3,
        'payload' : 'sen'
      },
      {
        'content_type' : 'text',
        'title' : O4,
        'payload' : 'wom'
      }
    ]
    }
    })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def Options(RecipientID, Text, OP1, OP2):
    print(('Sending  options to {0}').format(RecipientID))
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient' : {
        'id' : RecipientID
        },
        'message': {
            'attachment' : {
                'type' : 'template',
                'payload' : {
                    'template_type' : 'button',
                    'text': Text,
                    'buttons': [
                    {
                        'type' : 'postback',
                        'title' : OP1,
                        'payload' : 'start'
                    },
                    {
                        'type' : 'postback',
                        'title' : OP2,
                        'payload' : 'explain'
                    }]
                }
            }
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages?access_token=' + PAT, headers = headers, data = data)
    if r.status_code != 200:
        print(r.text)

def GenericTemplateOptions(RecipientID):
    print(('Sending  options to {0}').format(RecipientID))
    headers = {
    'Content-Type' : 'application/json'
    }
                                
    data = json.dumps({
        'recipient':{
        'id' : RecipientID
        },
        'message' : {
            'attachment' : {
            'type' : 'template',
            'payload' : {
            'template_type' : 'generic',
            'elements' : [
                {
            'title' : 'Get Voter information',
            'image_url' : 'https://c1.staticflickr.com/5/4219/34872765202_148d73b973_c.jpg',
            'subtitle': 'Get to know your voter requirements or set a reminder',
                'buttons' : [
                    {
                        'type' : 'postback',
                        'payload' : 'voters',
                        'title' : 'Voter Requirements'
                    },
                    {
                        'type' : 'postback',
                        'payload' : 'registration',
                        'title' : 'Know your voting status.'
                    },
                     {
                        'type' : 'postback',
                        'payload' : 'reminder',
                        'title' : 'Set A Reminder'
                    }              
                             
                
                ]},
                {
            'title' : 'Know your candidates',
            'image_url' : 'https://farm5.staticflickr.com/4250/34872749292_ffd4cc9444_o_d.jpg',
            'subtitle': 'Get information on who is vying.',
                'buttons' : [
                    {
                        'type' : 'web_url',
                        'url' : 'https://www.standardmedia.co.ke/elections2017/news',
                        'title' : 'Get election News',
                        "webview_height_ratio": "tall"
                    }
                    ,{
                        'type' : 'postback',
                        'payload' : 'levels',
                        'title' : 'Choose an Election Level'
                    },
                
                ]},
                {
            'title' : 'Goverment Review',
            'image_url' : 'https://farm5.staticflickr.com/4221/34872757372_26a343544c_o_d.jpg',
            'subtitle': 'Get information about your county administration, or take a survey about them',
                'buttons' : [
                    {
                        'type' : 'postback',
                        'payload' : 'survey',
                        'title' : 'Review your county administration'
                    },
                    {
                        'type' : 'postback',
                        'payload' : 'contact',
                        'title' : 'Contact your county administration'
                    }              
                
                ]}
                ]
        }}}})
    r = requests.post('https://graph.facebook.com/v2.9/me/messages?access_token=' + PAT, headers = headers, data = data)
    if r.status_code != 200:
        print(r.text)

def LevelTemplateOptions(RecipientID, TXT1, TXT2, TXT3, TXT4, TXT5, TXT6, TXT7, TXT8, OP1, OP, OP3, OP4, OP5):
    print(('Sending  options to {0}').format(RecipientID))
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient':{
        'id' : RecipientID
        },
        'message' : {
            'attachment' : {
            'type' : 'template',
            'payload' : {
            'template_type' : 'generic',
            'elements' : [
                {
            'title' : TXT1,
            'image_url' : 'https://farm5.staticflickr.com/4197/34904964391_4266fb0521_b_d.jpg',
            'subtitle': TXT2,
                'buttons' : [
                    {
                        'type' : 'postback',
                        'payload' : 'pres',
                        'title' : OP1
                    },
                    {
                        'type' : 'postback',
                        'payload' : 'poll',
                        'title' : OP
                    }
                ]},
                {
            'title' : TXT3,
            'image_url' : 'https://farm5.staticflickr.com/4197/35036869425_4fd1bbe1fd_o_d.jpg',
            'subtitle': TXT4,
                'buttons' : [
                    {
                        'type' : 'postback',
                        'payload' : 'gov',
                        'title' : OP3
                    }             
                
                ]},
                {
            'title' : TXT5,
            'image_url' : 'https://farm5.staticflickr.com/4223/35036874755_6e1a91296d_z_d.jpg',
            'subtitle': TXT6,
                'buttons' : [
                    
                    {
                        'type' : 'postback',
                        'payload' : 'senate',
                        'title' : OP4
                    }              
                
                ]},
                {
                'title' : TXT7,
            'image_url' : 'https://farm5.staticflickr.com/4243/34904966591_db66e618ba_z_d.jpg',
            'subtitle': TXT8,
                'buttons' : [
                    {
                        'type' : 'postback',
                        'payload' : 'womrep',
                        'title' : OP5
                    }
                ]}
                ]
        }}}})
    r = requests.post('https://graph.facebook.com/v2.9/me/messages?access_token=' + PAT, headers = headers, data = data)
    if r.status_code != 200:
        print(r.text)

def TakeSurvey(RecipientID, Text, URL, OP1):
    print(('Sending message to {0}').format(RecipientID))

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient' : {
        'id' : RecipientID
        },
        'message': {
            'attachment' : {
                'type' : 'template',
                'payload' : {
                    'template_type' : 'button',
                    'text': Text,
                    'buttons': [
                    {
                        'type' : 'web_url',
                        'url' : URL,
                        'title' : OP1,
                        "webview_height_ratio": "tall",
                        "messenger_extensions": true  
                    }]
                }
            }
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def WebView(RecipientID, Text, URL, OP1):
    print(('Sending message to {0}').format(RecipientID))

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient' : {
        'id' : RecipientID
        },
        'message': {
            'attachment' : {
                'type' : 'template',
                'payload' : {
                    'template_type' : 'button',
                    'text': Text,
                    'buttons': [
                    {
                        'type' : 'web_url',
                        'url' : URL,
                        'title' : OP1,
                        "webview_height_ratio": "tall",
                        "messenger_extensions": True  
                    }]
                }
            }
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def SendAttachment(RecipientID, Type, Link):
    print(('Sending message to {0}').format(RecipientID))

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient' : {
        'id' : RecipientID
        },
        'message': {
            'attachment' : {
                'type' : Type,
                'payload' : {
                    'url' : Link,
                }
            }
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def FindingUser(ID):
    headers = {
    'Content-Type' : 'application/json'
    }
    r = requests.post('https://graph.facebook.com/v2.9/' + ID + '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=' + PAT, headers=headers)
    print(r)
    return r

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

def FindingUser(ID):
    headers = {
    'Content-Type' : 'application/json'
    }
    r = requests.post('https://graph.facebook.com/v2.9/' + ID + '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=' + PAT, headers=headers)
    print(r)
    return r


def UsingWit(TEXT):
    response = client.message(TEXT)
    entity = None
    value = None

    try:
        entity = list(response['entities'])[0]
        if entity == 'names':
            value = response['entities'][entity][0]['value']
            return value
        elif entity == 'location':
            value = response['entities'][entity][0]['value']
            return value
        else:
            pass
    except Exception as e:
        raise e

#def Search(url):

#week = sched.add_job(OneWeek, 'date', run_date = datetime(2017, 8, 1, 12, 00))
#day = sched.add_job(TwoDays, 'date', run_date = datetime(2017, 8, 6, 12, 00))

def Level(text):
    if text in options:
        ResponseStack.append(text)
        level = ResponseStack.pop()
        return level

def OneWeek():
    return True

def TwoDays():
    return True

def Candidates(Level):
    candidate = '\n'.join([str(cand) for cand in Level])
    return candidate

def CheckListLength(text):
    if len(text) > 7:
        names = len(text)//2
        return text[:names], text[names:]
    else:
        pass

def CheckTextLength(text):
    l = 640
    if len(text) > l:
        texts = len(text)//2
        return text[:texts], text[texts:]
    else:
        pass

if __name__ == '__main__':
    #sched.start()
    app.run(debug = True)


g_nairobi = ['Evans Kidero - CORD-ODM', 'Mike Mbuvi Sonko - Jubilee']
g_evans_info = '''Evans Odhiambo Kidero is a Kenyan politician and current Governor of Nairobi County. 
He served as CEO of Mumias Sugar Company for 8 years, resigning in 2012 to join elective politics. 
Kidero was elected as the first governor of Nairobi County in the Nairobi gubernatorial elections of 2013 on an ODM ticket. 
Dr. Kidero is married to Susan Mboya, daughter of the late Kenyan politician, Tom Mboya, and together they have 3 children.'''

g_mike_info = '''Mbuvi Gidion Kioko Mike Sonko  commonly known as Mike Sonko is a Kenyan politician who currently serves as Senator of Nairobi. 
Sonko is the immediate former Member of Parliament for Makadara Constituency, Kenya, a position he was elected to on September 20, 2010 in a by-election. 
Born in Mombasa ,Mbuvi became the First Senator of Nairobi.
His style of leadership has been described as different and has earned him titles like, mtu wa watu (A man of the people).
'''