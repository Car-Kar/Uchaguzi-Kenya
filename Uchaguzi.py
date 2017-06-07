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
import base64
from kiswa import *

app = Flask(__name__)


#sched = Scheduler()


PAT = 'EAAarLkMVMy4BAERvNFAqZBaIfdpnrILzYWnLXeUhst52bj6d6oiA3YewwP7UvhDDGHdWciSElZCtZAWNnN15IbCZB10kepGG0BbkwAErwzi3jWnPZA6tPSh985a2j38lcrhRTNFFNaWZAvy6qv2FejYK7ZCaqgSXZCKm5D9V0vsj0QZDZD'
VerifyToken = '0454'
WitToken = 'DYIOAENA3VUYMZ2QHFQ6OX3AOZ3P3D3V'
client = Wit(access_token = WitToken)

SurveyUrl = 'https://m.me/672849446250204/?ref=f258b3c90e014ce15030df0a91a0a322'



IntroductoryMessage = ''' The 2017 Kenyan National Elections are taking place in August.
I am a tool for you to acquire more information on voting and the vying candidates.
'''
IntroductoryMessage2 = '''I provide information on voting procedures, voter registration, your county administration, the vying candidates, and government .
I have a top-level menu which you can access at any time by pressing the menu icon (\u2630)  at the bottom to choose the option that you want.
\U0001F642
'''
KiswahiliIntroduction2 = '''Nitakupa taarifa kuhusu taratibu kupiga kura, usajili wa wapiga kura, utawala wa kata yako, wagombea wanaogombea na ukaguzi wa serikali.
Nina orodha ambayo unaweza kupata wakati wowote kwa kubonyeza menu (\u2630) hapo chini ili kuchagua chaguo unataka.
\U0001F642'''
KiswahiliIntroduction = '''Jambo!
Uchaguzi wa Taifa wa Kenya unafanyika Agosti.
Mimi ni chombo kwa ajili ya wewe kupata taarifa zaidi juu ya kupiga kura na wagombea wanaogombea.
'''
VoterRegistration = '''Thank you for using Uchaguzi!
However due to logistical circumstances, the option of finding out your registration status is not available right now.
Please check again in a little while as we go about incorporating it.
'''
KG = '''Asante kwa kutumia Uchaguzi!
Hata hivyo kutokana na mazingira vifaa, chaguo la kutafuta hali yako ya usajili haipatikani kwa sasa.
Tafadhali angalia tena baada ya muda mfupi kama sisi kwenda juu kuchanganya yake.'''

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
We are only supporting ten counties right now; Kisumu, Mombasa, Nairobi, Kakamega, Turkana, Narok, Kericho, Kiambu, Nakuru, and Uasin Gishu.
Please check back from time to time as we integrate more counties!
\U0001F642
'''
ApologyMessage = '''
Sorry, I didn't get that.
Would you mind repeating it?
'''

Counties = ['kiambu', 'kisumu', 'mombasa', 'nairobi', 'nakuru', 'kakamega', 'uasin gishu', 'turkana', 'narok', 'kericho']
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
Kiswahili = False
uri = 'mongodb://MC:se*8DGs6t8F*39*k@ds149491.mlab.com:49491/uchaguzike'
ys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


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
    def IncomingLevels(self, FromUser, data):
        collection = self.DB['levels']
        print('Connected to levels collection!')
        user =  collection.find_one({'fromuser': FromUser})
        if user is not None and data in options:
            collection.update_one({'fromuser' : FromUser}, {'$set': {'level': data}})
            level = data.lower()
            return level

        elif user is not None:
            level = user['level']
            return level

        else:
            if data in options:
                collection.insert({'fromuser' : FromUser, 'level': data})
                level = data.lower()
                return level

    def IncomingCounties(self, FromUser, data):
        collection = self.DB['counties']
        print('Connected to counties collection!')
        user =  collection.find_one({'fromuser': FromUser})
        if user is not None and data in Counties:
                collection.update_one({'fromuser' : FromUser}, {'$set': {'county': data}})
                county = data.lower()
                return county
        elif user is not None :
                county = user['county']
                return county
        else:
            if data in options:
                collection.insert({'fromuser' : FromUser, 'county': data})
                county = data.lower()
                return county
            
            
    

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
        user =  collection.find_one({'name': pres})
        if user is not None:
            votes = user['votes']
            collection.update_one({'name' : pres}, {'$set': {'votes': votes + 1}})
            print(votes)
        else:
            collection.insert_one({'name' : pres, 'votes': 1})

    

class UsingSQL:
    def __init__(self):
        self.conn = ''
        self.curs = ''

    def SQLConnection(self):
        try:
            self.conn = pymysql.connect(user='b5ad6687738858',passwd='23bfecef',host = 'us-cdbr-iron-east-03.cleardb.net', database='heroku_611862edb2b2330')
            self.curs = self.conn.cursor()
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
        return result

    def all_presidential_names(self):
        self.curs.execute("""SELECT name FROM presidential_candidates""")
        results = self.curs.fetchall()
        candidates = []
        for row in results:
            candidates.append(row[0])
        return candidates

    def all_governor_names(self):
        self.curs.execute("""SELECT name FROM governor_candidates""")
        results = self.curs.fetchall()
        candidates = []
        for row in results:

            candidates.append(row[0])
        return candidates

    def all_senator_names(self):
        self.curs.execute("""SELECT name FROM senators""")
        results = self.curs.fetchall()
        candidates = []
        for row in results:
            candidates.append(row[0])
        return candidates

    def all_rep_names(self):
        self.curs.execute("""SELECT name FROM women_reps""")
        results = self.curs.fetchall()
        candidates = []
        for row in results:
            candidates.append(row[0])
        return candidates

    def president_bio(self, value):
        self.curs.execute("""SELECT running_mate, political_bio, image FROM presidential_candidates WHERE UPPER(name) Like  UPPER('%s') """ % (value))
        result = self.curs.fetchall()
        mate = []
        bio = []
        for row in result:
            print(row[0])
            print(row[1])
            print(row[2])
            return row[0], row[1], row[2]

    def governor_bio(self, value1, value2):
        self.curs.execute("""SELECT running_mate, political_bio, image FROM governor_candidates WHERE UPPER(name) Like  UPPER('%s') && UPPER(county) Like UPPER('%s') """ % (value1,value2))
        result= self.curs.fetchall()
        for row in result:
            return row[0], row[1], row[2]

    def governors(self, value):
        self.curs.execute("""SELECT name, political_party FROM governor_candidates WHERE UPPER(county) Like  UPPER('%s') """ % (value))
        results = list(self.curs.fetchall())
        result = '\n'.join([str(cand) for cand in results])
        result = result.replace('(', ' ')
        result = result.replace(')', ' ')
        result = result.replace("'", ' ')
        result = result.replace(',', '-')
        return result

    def senators(self, value):
        self.curs.execute("""SELECT name, political_party FROM senators WHERE UPPER(county) Like  UPPER('%s') """ % (value))
        results = list(self.curs.fetchall())
        result = '\n'.join([str(cand) for cand in results])
        result = result.replace('(', ' ')
        result = result.replace(')', ' ')
        result = result.replace("'", ' ')
        result = result.replace(',', '-')
        return result

    def senators_bio(self, value1, value2):
        self.curs.execute("""SELECT political_bio, image FROM senators WHERE UPPER(name) Like  UPPER('%s')&& UPPER(county) Like UPPER('%s') """ % (value1,value2))
        result = self.curs.fetchall()
        for row in result:
            return row[0], row[1]

    def women_reps(self, value):
        self.curs.execute("""SELECT name FROM women_reps WHERE UPPER(county) Like  UPPER('%s') """ % (value))
        results = list(self.curs.fetchall())
        result = '\n'.join([str(cand) for cand in results])
        result = result.replace('(', ' ')
        result = result.replace(')', ' ')
        result = result.replace("'", ' ')
        result = result.replace(',', '-')
        return result

    def women_reps_bio(self, value1, value2):
        self.curs.execute("""SELECT political_bio, image FROM women_reps WHERE UPPER(name) Like  UPPER('%s')&& UPPER(county) Like UPPER('%s') """ % (value1,value2))
        result = self.curs.fetchall()
        for row in result:
            return row[0], row[1]

    def CloseConnection(self):
        self.conn.close()
        print('MySQL connection closed!')






MDB = UsingMongo()
SQL = UsingSQL()
Options = ['haha']
options = ['pres', 'gov', 'senate', 'womrep', 'vote', 'contact', 'survey', 'cs']
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
                    if (msg.get('message')) or  (msg.get('postback')):
                        print(msg)
                        SenderID = msg['sender']['id']
                        nme = FindingUser(SenderID)
                        response = None
                        UserSays = ReturnType(msg)
                        print(UserSays)
                        surveying = False
                        Kiswahili = MDB.IncomingKiswahiliUsers(SenderID, UserSays)
                        level = MDB.IncomingLevels(SenderID, UserSays.lower())
                        counties = MDB.IncomingCounties(SenderID, UserSays)
                        county = [c for c in Counties if UserSays.lower() in c.lower()]
                        county = ' '.join(county)
                        print(county)
                        cands = FindingCandidate(level, UserSays)
                        print(cands)
                        #News = MDB.NewsSubscribers(SenderID, UserSays)
                        #print(Kiswahili)
                        print(level)
                        racer = DefiningRace(UserSays)
                        print(racer)
                        Start = 'Hello ' + nme + '! What language do you want to continue in?'
                    
                        if msg.get('message'):
                            if Kiswahili is not True and county is not None and level == 'cs':
                                url = countydict[county]
                                Voting(SenderID, 'Choose an option below', '\U000FEB0A Take a short survey', url, '\U000FE524 County Contacts')

                            if 'start' in UserSays.lower() or 'hey' in UserSays.lower() or 'hi' == UserSays.lower() or 'hello' in UserSays.lower():
                                level = None
                                ReusableOptions(SenderID, Start, 'Kiswahili', 'English')

                            if Kiswahili == True and 'swahili' in UserSays.lower():
                                level = None
                                SendMessage(SenderID, KiswahiliIntroduction)
                                SendMessage(SenderID, KiswahiliIntroduction2)
                                GenericTemplateOptions(SenderID, 
                                'Kupiga Kura', 'Tunakupa mawaidha kuhusu kupiga kura',
                                'Mahitaji ya Kura', 'Umesajiliwa?', 'Weka Mawaidha',
                                'Wagombea', 'Jua nani anagombea cheo cha serikali',
                                'Ujumbe kuhusu uchaguzi',
                                'Chagua cheo cha kura',
                                'Serikali', 
                                'Pata ujumbe kuhusu serikali ya kata yako.',
                                'Kagua Serikali'
                                )
                            if Kiswahili is not True and 'english' in UserSays.lower():
                                level = None
                                SendMessage(SenderID, IntroductoryMessage)
                                SendMessage(SenderID, IntroductoryMessage2)
                                GenericTemplateOptions(SenderID,
                                'Voter Information',
                                'We give you information on voting in the elections.',
                                'Voter Requirements',
                                'Voter Registration',
                                'Set a reminder',
                                'Elections 2017',
                                'Latest Election News',
                                'Know your candidates for the coming elections',
                                'Elections Levels',
                                'Government Review',
                                'Talk to your county government',
                                'County Review'
                                )

                            if Kiswahili == True and 'nipe' in UserSays.lower():
                                level = None
                                SendMessage(SenderID, VoterRequirements)
                            if Kiswahili == True and 'mawaidha' in UserSays.lower():
                                level = None
                                response = '''Nitakutumia alani ya kukukumbusha siku ya uchaguzi.
                                Unataka alani ya siku gani?'''
                                ReusableOptions(SenderID, response, 'A Week Before', 'Two Days Before')

                            if level == 'vote' and UserSays.lower() in racer.lower():
                                MDB.PresidentialRace(racer.capitalize())
                                SendMessage(SenderID, 'Thank you for voting!')
                                HomeTemplate(SenderID, 'Do you want to see the results, go back home, or say goodbye?', 'Home', 'Results')
                        
                        
                        

                            if Kiswahili is not True and 'a week' in UserSays.lower():
                                response = 'I will be messaging you a week before the elections as a reminder'
                                SendMessage(SenderID, response)
                                Home(SenderID, 'Go back to home?', 'Home')

                            if Kiswahili is not True and 'two days' in UserSays.lower():
                                response = 'I will be messaging you two days before the elections as a reminder'
                                SendMessage(SenderID, response)
                                Home(SenderID, 'Go back to home?', 'Home')
                            if Kiswahili is True and 'siku mbili' in UserSays.lower():
                                response = 'Nitakupa alani siku mbili kabla ya uchaguzi.'
                                SendMessage(SenderID, response)
                                Home(SenderID, 'Rudi Mwanzo?', 'Mwanzo')
                            if Kiswahili is True and 'wiki' in UserSays.lower():
                                response = 'Nitakupa alani wiki moja kabla ya uchaguzi.'
                                SendMessage(SenderID, response)
                                Home(SenderID, 'Rudi Mwanzo?', 'Mwanzo')

                        
                            if Kiswahili is not True and 'home' in UserSays.lower():
                                GenericTemplateOptions(SenderID,
                                'Voter Information',
                                'We give you information on voting in the elections.',
                                'Voter Requirements',
                                'Voter Registration',
                                'Set a reminder',
                                'Elections 2017',
                                'Know your candidates for the coming elections',
                                'Latest Election News',
                                'Elections Levels',
                                'Government Review',
                                'Talk to your county government',
                                'County Review'
                                )
                            elif Kiswahili is True and 'mwanzo' in UserSays.lower():
                                GenericTemplateOptions(SenderID, 
                                'Kupiga Kura', 'Tunakupa mawaidha kuhusu kupiga kura',
                                'Mahitaji ya Kura', 'Umesajiliwa?', 'Weka Mawaidha',
                                'Wagombea', 'Jua nani anagombea cheo cha serikali',
                                'Ujumbe kuhusu uchaguzi',
                                'Chagua cheo cha kura',
                                'Serikali', 
                                'Pata ujumbe kuhusu serikali ya kata yako.',
                                'Kagua Serikali'
                                )

                            elif 'bye' in UserSays.lower():
                                SendMessage(SenderID, Goodbye)

                            elif Kiswahili is not True and level == 'pres' and UserSays.lower() in cands.lower():
                                query = '%' + UserSays.lower() + '%'
                                run, bio, img = SQL.president_bio(query)
                                bio = str(bio)
                                SendAttachment(SenderID, 'image', img)
                                if len(str(run)) < 1:
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                else:
                                    running_mate = 'His running mate is ' + str(run)
                                    SendMessage(SenderID, running_mate)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                            elif Kiswahili is True and level == 'pres':
                                if  'uhuru' in UserSays.lower() or 'kenyatta' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('%uhuru%')
                                    bio = uk
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')
                                elif  'raila' in UserSays.lower() or 'amollo' in UserSays.lower() or 'odinga' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('%raila%')
                                    bio = rk
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')

                                elif  'mohamed' in UserSays.lower() or 'diba' in UserSays.lower() or 'adbuba' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('mohamed%')
                                    bio = mdk
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')
                                elif  'khwa' in UserSays.lower() or 'jirongo' in UserSays.lower() or 'shakhalaga' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('%khwa%')
                                    bio = kwk
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')
                                elif  'aukot' in UserSays.lower() or 'ekuru' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('%ekuru%')
                                    bio = aek
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')
                                elif  'justus' in UserSays.lower() or 'zakayo' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('%justus%')
                                    bio = uk
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')
                                elif  'peter' in UserSays.lower() or 'solomon' in UserSays.lower() or 'gichira' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('%gichira%')
                                    bio = psk
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')
                                elif  'amram' in UserSays.lower() or 'inyambuki' in UserSays.lower():
                                    run, bio, img = SQL.president_bio('%amram%')
                                    bio = amk
                                    SendAttachment(SenderID, 'image', img)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani.''',
                                  '\U000FE4B0 Nyumbani')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Je, unataka kujua kuhusu mgombea nyingine, au kurejea nyumbani?
Kama unataka kujua kuhusu mgombea mwingine, nitumie yake au jina lake, vinginevyo bofya kitufe hapo chini kwenda nyumbani''',
                                  '\U000FE4B0 Nyumbani')
                                else:
                                    SendMessage(SenderID, 'Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi.')

                            elif level == 'senate' and UserSays.lower() in cands.lower():
                                query = '%' + UserSays.lower() + '%'
                                county = '%' + county + '%'
                                bio, img = SQL.senators_bio(query, county)
                                bio = str(bio)
                            
                                SendAttachment(SenderID, 'image', img)
                                if len(bio) > 640:
                                    bio, bios = CheckTextLength(bio)
                                    response = bio + '-'
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, bios)
                                    HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
                                 If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                else:
                                    SendMessage(SenderID, bio)
                                    HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
                                 If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                            elif level == 'womrep' and UserSays.lower() in cands.lower():
                                query = '%' + UserSays.lower() + '%'
                                county = '%' + county + '%'
                                bio, img = SQL.women_reps_bio(query, county)
                                bio = str(bio)
                                print(bio)
                                SendAttachment(SenderID, 'image', img)
                                if len(bio) > 640:
                                    bio, bios = CheckTextLength(bio)
                                    response = bio + '-'
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, bios)
                                    HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                else:
                                    SendMessage(SenderID, bio)
                                    HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                            elif level == 'gov' and UserSays.lower() in cands.lower():
                                
                                query = '%' + UserSays.lower() + '%'
                                county = '%' + county + '%'
                                run, bio, img = SQL.governor_bio(query, county)
                                SendAttachment(SenderID, 'image', img)
                                bio = str(bio)
                                if len(str(run)) < 1:
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
                                 If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                else:
                                    running_mate = 'His running mate is ' + str(run)
                                    SendMessage(SenderID, running_mate)
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  '\U000FE4B0 Home')

                            elif level == 'vote' and UserSays.lower() in racer.lower():
                                print('Im')

                            elif Kiswahili is not True and 'gov' == level:
                                query = '%' + county + '%'
                                candidates = SQL.governors(query)
                                if len(candidates) > 640:
                                    first_names, second_names = CheckListLength(candidates)
                                    response = 'The gubernatorial candidates for ' + county + ' are: \n' + str(first_names[0:])
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, second_names)
                                    SendMessage(SenderID, CandidateMoreInfo)
                                else:
                                    response = 'The gubernatorial candidates for ' + county + ' are: \n' + str(candidates[0:])
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, CandidateMoreInfo)

                            elif Kiswahili is not True and 'senate' == level:
                                query = '%' + county + '%'
                                candidates = SQL.senators(query)
                                if len(candidates) > 640:
                                    first_names, second_names = CheckListLength(candidates)
                                    response = 'The senate candidates are: \n' + str(first_names[0:])
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, second_names)
                                    SendMessage(SenderID, CandidateMoreInfo)
                                else:
                                    response = 'The senate candidates for ' + county + ' are: \n' + str(candidates[0:])
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, CandidateMoreInfo)

                            elif Kiswahili is not True and 'womrep' == level:
                                query = '%' + county + '%'
                                candidates = SQL.women_reps(query)
                                if len(candidates) > 640:
                                    first_names, second_names = CheckListLength(candidates)
                                    response = 'The  candidates are: \n' + str(first_names[0:])
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, second_names)
                                    SendMessage(SenderID, CandidateMoreInfo)
                                else:
                                    response = 'The candidates for ' + county + ' are: \n' + str(candidates[0:])
                                    SendMessage(SenderID, response)
                                    SendMessage(SenderID, CandidateMoreInfo)
                        
                            elif Kiswahili is not True and 'nairobi' == UserSays.lower() and 'senate' == level:
                                query = '%nairobi%'
                                candidates = SQL.senators(query)
                                first_names, second_names = CheckListLength(candidates)
                                response = 'The senate candidates in Nairobi are: \n' + str(first_names[0:])
                                SendMessage(SenderID, response)
                                SendMessage(SenderID, second_names)
                                SendMessage(SenderID, CandidateMoreInfo)
                            
                            elif level == 'contact' and county is not None:
                                contacts = countydict[county]
                                print(contacts)

                            elif Kiswahili is not True and UserSays.lower() == 'yes' or UserSays.lower() == 'no':
                                SendMessage(SenderID, 'On a scale of 1 - 10, how effective would you rate your county government.')

                            elif Kiswahili is not True and level == 'survey' and UserSays in ys:
                                    print('hehehe')
                                    Home(SenderID, 'Thank you for taking our survey!', '\U000FE4B0 Home')

                                

                        elif msg.get('postback'): 

                            if UserSays == 'Get Started':
                                ReusableOptions(SenderID, Start, 'Kiswahili', 'English')

                            if Kiswahili == True and UserSays == 'survey':
                                TakeSurvey(SenderID, 'Tafadhali Jibu maswali haya ili - review them.', SurveyUrl, 'SurveyName')
    
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
                            if Kiswahili is True and UserSays == 'levels':
                                LevelTemplateOptions(SenderID,
                                'Urais',
                                'Fahamu wanaogombea wagombea urais na wenzi wao kukimbia.',
                                'Gavana',
                                'Fahamu wanaogombea ugavana urais na wenzi wao kukimbia.',
                                'Wagombea seneta',
                                'Fahamu wanaogombea wagombea useneta na wenzi wao kukimbia.',
                                'Wawakilishi wa Wanawake',
                                'Fahamu wanaogombea wagombea.',
                                'Wagombea Urais',
                                'Kagua wagombea',
                                'Wagombea ugavana',
                                'Wagombea useneta',
                                'Wawakilishi wa wanawake'
                                )
                            if Kiswahili is not True and UserSays == 'voters':
                                SendMessage(SenderID, VoterRequirements )
                                SendMessage(SenderID, 'Here are some helpful graphics to help you.')
                                SendAttachment(SenderID, 'video', '')
                            
                                SendAttachment(SenderID,'image', 'https://farm5.staticflickr.com/4248/34872766342_a66c0fa485_o_d.jpg')
                                SendMessage(SenderID, ContinueUsing)
                                HomeP(SenderID, 'Go back to home, or do you want to say goodbye?', '\U000FE4B0 Home')
                            if Kiswahili is True and UserSays == 'voters':
                                SendMessage(SenderID, KiswahiliRequirements)
                                SendAttachment(SenderID,'image', 'https://farm5.staticflickr.com/4248/34872766342_a66c0fa485_o_d.jpg')
                                HomeP(SenderID, 'Unataka kurudi mwanzo?', '\U000FE4B0 Mwanzo')


                            elif Kiswahili is not True and UserSays == 'poll':
                                ButtonTemplate(SenderID, 'You can vote or see the results of the current polling.',
                             '\u2705 Vote',
                             '\U0001F4CB Results')

                            elif Kiswahili is not True and UserSays == 'registration':
                                SendAttachment(SenderID, 'image', 'https://farm5.staticflickr.com/4243/34193089344_55a2249bd6_o_d.jpg')
                                
                                SendMessage(SenderID, VoterRegistration)
                                HomeP(SenderID, 'Go back to home, or do you want to say goodbye?', '\U000FE4B0 Home')

                            elif Kiswahili is True and UserSays == 'registration':
                                SendAttachment(SenderID, 'image', 'https://farm5.staticflickr.com/4243/34193089344_55a2249bd6_o_d.jpg')
                                
                                SendMessage(SenderID, KG)
                                HomeP(SenderID, 'Unataka kurudi mwanzo?', '\U000FE4B0 Mwanzo')

                    
                            if Kiswahili == True and 'reminder' in UserSays.lower():
                                response = '''Nitakutumia alani ya kukukumbusha siku ya uchaguzi.
                                Unataka alani ya siku gani?'''
                                ReusableOptions(SenderID, response, 'Wiki moja kabla.', 'Siku mbili.')

                            elif Kiswahili is not True and UserSays == 'pres':
                                candidates = SQL.all_presidential_candidates()
                                print(candidates)
                                first_names, second_names = CheckListLength(candidates)
                                response = 'The presidential candidates are: \n' + str(first_names[0:])
                                SendMessage(SenderID, response)
                                SendMessage(SenderID, second_names)
                                SendMessage(SenderID, CandidateMoreInfo)
                            elif Kiswahili is  True and UserSays == 'pres':
                                candidates = SQL.all_presidential_candidates()
                                first_names, second_names = CheckListLength(candidates)
                                response = 'Wagombea urais ni: \n' + str(first_names[0:])
                                SendMessage(SenderID, response)
                                SendMessage(SenderID, second_names)
                                SendMessage(SenderID, 'Unataka kujua zaidi kuhusu moja ya wagombea hawa? Nitumie jina lake.')


                            elif Kiswahili is not True and UserSays == 'gov':
                                SendMessage(SenderID, CountiesMessage)
                                CountyOptions(SenderID, 'Please choose one below.')

                            elif Kiswahili is not True and UserSays == 'senate':
                                SendMessage(SenderID, CountiesMessage)
                                CountyOptions(SenderID, 'Please choose one below.')

                            elif Kiswahili is not True and UserSays == 'womrep':
                                SendMessage(SenderID, CountiesMessage)
                                CountyOptions(SenderID, 'Please choose one below.')

                            elif Kiswahili is not True and UserSays == 'contact':
                                SendMessage(SenderID, CountiesMessage)
                                CountyOptions(SenderID, 'Please choose one below.')

                            elif Kiswahili is not True and 'vote' in UserSays.lower():
                                SendMessage(SenderID, 'If the elections happened tomorrow, which presidential candidate would you vote for?')

                            elif Kiswahili is not True and 'home' in UserSays.lower():
                                GenericTemplateOptions(SenderID,
                                'Voter Information',
                                'We give you information on voting in the elections.',
                                'Voter Requirements',
                                'Voter Registration',
                                'Set a reminder',
                                'Elections 2017',
                                'Know your candidates for the coming elections',
                                'Latest Election News',
                                'Elections Levels',
                                'Government Review',
                                'Talk to your county government',
                                'County Review'
                                )

                            elif 'cs' == UserSays:
                                SendMessage(SenderID, 'What county are you from?')
                                CountyOptions(SenderID, 'Choose one below')

                            elif Kiswahili is not True and level == 'survey' and UserSays == 'survey':
                                SendMessage(SenderID, 'Please answer the following few questions.')
                                ReusableOptions(SenderID, 'Are you familiar with your county administration?', 'Yes', 'No')

                            elif Kiswahili is True and 'home' in UserSays.lower():
                                GenericTemplateOptions(SenderID, 
                                'Kupiga Kura', 'Tunakupa mawaidha kuhusu kupiga kura',
                                'Mahitaji ya Kura', 'Umesajiliwa?', 'Weka Mawaidha',
                                'Wagombea', 'Jua nani anagombea cheo cha serikali',
                                'Ujumbe kuhusu uchaguzi',
                                'Chagua cheo cha kura',
                                'Serikali', 
                                'Pata ujumbe kuhusu serikali ya kata yako.',
                                'Kagua Serikali'
                                )

                            elif Kiswahili is True and level is not None:
                                if (level == 'gov' or level == 'sen' or level == 'womrep'):
                                    SendAttachment(SenderID, 'image', 'https://media.giphy.com/media/RFgY2jhk6xKzS/giphy.gif')
                                    HomeP(SenderID, 'Kiswahili hakitumiki na hatua hii. Endelea na Kiingereza?', '\U0001F44D Sawa')





        SQL.CloseConnection()
                        
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
        if msg['message'].get('text'):
            MessageText = msg['message']['text']
            print(MessageText)
            return MessageText
        elif msg['message'].get('attachments'):
            text = 'image'
            return text
    elif msg.get('postback'):
        if msg.get('postback').get('payload'):
            PostbackText = msg['postback']['payload']
            print(PostbackText)
            return PostbackText
    elif msg.get('web_url'):
        URLText = msg['web_url']['title']
        return URLText
        print(URLText)
    else:
        pass
    

def DefiningRace(name):
    candidates = SQL.all_presidential_names()
    result = [c for c in candidates if name.lower() in c.lower()]
    result = ' '.join(result)
    return result.lower()

def FindingCandidate(level, name):
    if level == 'pres':
        candidates = SQL.all_presidential_names()
        result = [c for c in candidates if name.lower() in c.lower()]
        result = ' '.join(result)
        return result.lower()

    if level == 'gov':
        candidates = SQL.all_governor_names()
        result = [c for c in candidates if name.lower() in c.lower()]
        result = ' '.join(result)
        return result.lower()

    if level == 'senate':
        candidates = SQL.all_senator_names()
        result = [c for c in candidates if name.lower() in c.lower()]
        result = ' '.join(result)
        return result.lower()

    if level == 'womrep':
        candidates = SQL.all_rep_names()
        result = [c for c in candidates if name.lower() in c.lower()]
        result = ' '.join(result)
        return result.lower()


def HomeP(RecipientID, TXT, op1):
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient': {
        'id': RecipientID
    },
    'message' :  {
        'attachment' : {
        'type': 'template',
        'payload' : {
        'template_type' : 'button',
        'text': TXT,
        'buttons':[
      {
        'type': 'postback',
        'title' : op1,
        'payload' : 'home'
      }
    ]
    }
    }}})
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def Home(RecipientID, Text, op1):
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
      }
    ]
    }
    })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def Voting(RecipientID, A, B, C, D):
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        "recipient": {
        "id": RecipientID
    },
    "message": {
    "attachment": {
        "type": "template",
        "payload":{
        "template_type":"button",
        "text": A,
        "buttons":[
        {
            "type":"postback",
            "title": B,
            "payload": "survey"
          },
          {
            "type":"web_url",
            "url": C,
            "title": D          }
          
        ]
      }
    }
  }
    } 
    )
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)



def ButtonTemplate(RecipientID, A, B, C):
    

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        "recipient": {
        "id": RecipientID
    },
    "message": {
    "attachment": {
        "type": "template",
        "payload":{
        "template_type":"button",
        "text": A,
        "buttons":[
        {
            "type":"postback",
            "title": B,
            "payload": "vote"
          },
          {
            "type":"web_url",
            "url": "https://uchaguzi-ke.herokuapp.com",
            "title": C          }
          
        ]
      }
    }
  }
    } 
    )
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def HomeTemplate(RecipientID, A, B, C):

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        "recipient": {
        "id": RecipientID
    },
    "message": {
    "attachment": {
        "type": "template",
        "payload":{
        "template_type":"button",
        "text": A,
        "buttons":[
        {
            "type":"postback",
            "title": B,
            "payload": "home"
          },
          {
            "type":"web_url",
            "url": "https://uchaguzi-ke.herokuapp.com",
            "title": C          }
          
        ]
      }
    }
  }
    } 
    )
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

def GenericTemplateOptions(RecipientID, A, B, C, D, E, F, G, H, I, J, K, L):
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
            'title' : A,
            'image_url' : 'https://c1.staticflickr.com/5/4219/34872765202_148d73b973_c.jpg',
            'subtitle': B,
                'buttons' : [
                    {
                        'type' : 'postback',
                        'payload' : 'voters',
                        'title' : C
                    },
                    {
                        'type' : 'postback',
                        'payload' : 'registration',
                        'title' : D
                    },
                     {
                        'type' : 'postback',
                        'payload' : 'reminder',
                        'title' : E
                    }              
                             
                
                ]},
                {
            'title' : F,
            'image_url' : 'https://farm5.staticflickr.com/4250/34872749292_ffd4cc9444_o_d.jpg',
            'subtitle': G,
                'buttons' : [
                    {
                        'type' : 'web_url',
                        'url' : "https://www.standardmedia.co.ke/elections2017/news",
                        'title' : H,
                        "webview_height_ratio": "tall"
                    }
                    ,{
                        'type' : 'postback',
                        'payload' : 'levels',
                        'title' : I
                    },
                
                ]},
                {
            'title' : J,
            'image_url' : 'https://farm5.staticflickr.com/4221/34872757372_26a343544c_o_d.jpg',
            'subtitle': K,
                'buttons' : [
                    {
                        'type' : 'postback',
                        'payload' : 'cs',
                        'title' : L
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
    r = requests.get('https://graph.facebook.com/v2.9/' + ID + '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=' + PAT, headers=headers)
    nm = r.json()
    return nm['first_name']


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

def CountyOptions(RecipientID, TXT):
    print(('Sending countyoptions to {0}').format(RecipientID))
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
        'title' : 'Nairobi',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Kisumu',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Mombasa',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Kiambu',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Uasin Gichu',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Nakuru',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Kakamega',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Kericho',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Narok',
        'payload' : 'IsReusable'
      },
      {
        'content_type': 'text',
        'title' : 'Turkana',
        'payload' : 'IsReusable'
      }

    ]
    }
    })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)



if __name__ == '__main__':
    #sched.start()
    app.run(debug = True)

countydict = {'nairobi': 'http://www.nairobi.go.ke/home/subcounty-administration/',
'nakuru' : 'http://www.nakuru.go.ke/contactus/',
'kiambu' : 'http://www.kiambu.go.ke/contact-us',
'mombasa' : 'http://assembly.mombasa.go.ke/',
'kericho' : 'http://www.kericho.go.ke/pages/contact.html' ,
'turkana' : 'http://www.turkana.go.ke/index.php/governor/',
'kisumu' : 'http://kisumu.go.ke/contact' ,
'uasin gishu' : 'https://www.uasingishu.go.ke/?page_id=41' ,
'kakamega': 'https://kakamega.go.ke/contact-us/',
 'narok': 'http://www.narok.go.ke/contact-us' }



uk = '''Chama cha Kisiasa-Jubilee 
Mgombea mwenza-William Ruto 
Uhuru Muigai Kenyatta (alizaliwa 26 Oktoba 1961) ni 4 na Rais wa sasa wa Kenya, katika ofisi tangu 2013. Yeye ni mwana wa Jomo Kenyatta, rais wa kwanza wa Kenya, na mke wake wa nne Ngina Kenyatta. Uhuru Kenyatta alichaguliwa kuwa rais wa Kenya chini ya Alliance National (TNA), ambayo ilikuwa sehemu ya Jubilee Alliance na mgombea mwenza William Ruto la Umoja wa Republican Party (URP). Uhuru na Ruto walishinda 50.07% ya kura kutupwa, na wapinzani wa karibu, Raila Odinga na mgombea mwenza Kalonzo Musyoka wa Muungano wa Mageuzi na Demokrasia kupata 42%. Raila Amolo Odinga mgogoro matokeo ya uchaguzi katika Mahakama Kuu ambayo hata hivyo ilishikilia kwamba uchaguzi wa Uhuru ulikuwa halali na kama makosa kama ulikuwepo halikuleta tofauti na matokeo ya mwisho. Uhuru Kenyatta aliweza kuapishwa kama Rais tarehe 9 Aprili 2013.
'''

 
rk = '''Chama cha Kisiasa -ODM (NASA)
Mgombea mwenza-KALOZO MUSYOKA
Raila Amolo Odinga (alizaliwa Januari 7, 1945), pia maarufu kwa wafuasi wake kama Agwambo (maana yake "ajabu mkubwa"), Tinga (Luo na Kiswahili wa "trekta"), Baba (Kiswahili wa "baba"), RAO, ( kifupi namna ya 'Raila Amolo Odinga ") na Jakom (Luo kwa" Mwenyekiti ") ni mwanasiasa wa Kenya ambaye alikuwa Waziri Mkuu wa Kenya kutoka 2008 hadi 2013. alichaguliwa kama Mbunge wa Langata mwaka 1992, kuwahudumia kama Waziri wa Nishati na mwaka wa 2001 kwa 2002 na kuwa Waziri wa Barabara, Ujenzi wa Umma, na Makazi kutoka 2003 kwa 2005. Yeye alikuwa mkuu wa upinzani mgombea katika uchaguzi wa rais 2007, kukimbia dhidi anayemaliza muda wake Mwai Kibaki. Kufuatia uchaguzi na baada ya uchaguzi mgogoro vurugu-umeharibika, Odinga aliteuliwa kuwa Waziri Mkuu katika Aprili 2008 katika serikali ya mseto mkataba na Mwai Kibaki, kutumikia kama Msimamizi na Mratibu wa umoja wa kitaifa serikali ya mseto. Katika uchaguzi wa rais wa baadae miaka 5 baadaye nafasi ya pili dhidi ya Uhuru Kenyatta, Kibaki iliyopendelewa mrithi, garnering 5340546 kura, ambayo kuwakilishwa 43.28% ya kura zilizopigwa.
 '''
mdk = '''
Chama cha Kisiasa -ALLIANCE FOR REAL CHANGE
Mohammed Abduba Dida (alizaliwa 1974) ni mwalimu wa Kenya ambaye aliwania urais wa nchi mwaka 2013 uchaguzi wa rais juu ya ALLIANCE FOR REAL CHANGE. Dida hakuwa anajulikana kabla ya kuwasilisha yake ya magazeti ya IEBC. Kazi yake awali ilikuwa  kufundisha Kiingereza Fasihi na Dini katika shule ya Lenana na Daadab Shule ya Sekondari katika wakimbizi camp. Alifanikiwa  kupata  kura 52848 inayewakilisha 0.43% ya kura za wananchi.
'''

aek = ''' 
Chama cha Kisiasa -THIRDWAY ALLIANCE KENYA
Kwa Wakenya wengi, Ekuru ni mtu ambaye umaarufu wake  kitaifa  umepatikana kupitia kazi yake kama mkurugenzi wa Kamati ya “defunct” ya wataalamu wa Katiba. Yeye pia ni mwenyekiti wa wajumbe uteuzi jopo “headhunting” ya mwili mpya ya uchaguzi, Uchaguzi na Mipaka Tume Huru (IEBC). Ekuru pia Mshauri Maalum wa Serikali mpya ya Wizara ya Ulinzi ya Sudan Kusini. Hata kwa uteuzi high ofisi, Ekuru imekuwa moja ya mawakili kabisa kwa haki za makundi ya wachache kama vile wakimbizi, IDPs na jamii duni, hasa wale kutoka sehemu ya kaskazini ya nchi.

'''

kwk = '''
 
Chama cha Kisiasa -UNITED DEMOCRATIC PARTY
Cyrus Khwa Shakhalaga Jirongo alikuwa Mbunge aliyechaguliwa kuwakilisha Lugari kati ya 2008 na 2013/03/04 .Yeye alikuwa Mjumbe wa Umoja wa Maendeleo ya Kidemokrasia Kenya African mpaka 2013-01 .Yeye alikuwa mgombea wa Rais wa Jamhuri ya Kenya anayewakilisha Kenya kati 2012-09- 09 na 2012-12-04.Cyrus Khwa Shakhalaga Jirongo alikuwa Mwenyekiti wa Kenya African Union Development Kidemokrasia tangu 2007 .Yeye alikuwa Mbunge aliyechaguliwa kuwakilisha Lugari kati ya mwaka 1997 na 2002 .Cyrus Khwa Shakhalaga Jirongo alikuwa Mwenyekiti wa Vijana kwa KANU 1992 kati ya 1992 na 1992 .Yeye alikuwa Mwenyekiti wa AFC Leopards klabu kati ya 1991 na 1991 .Yeye alikuwa shahada ya kwanza mwanafunzi wa Chuo Kikuu cha Egerton kati ya 1982 na 1986 .Cyrus Khwa Shakhalaga Jirongo mara Secondary School Mwanafunzi wa Mangu High School kati ya mwaka 1978 na 1981 .Cyrus Khwa Shakhalaga Jirongo mara mjumbe wa Kamati ya Uwekezaji Umma - SO 188 kati ya 2008 na 2012.
'''
jxk = '''
Chama cha Kisiasa -JUSTICE AND FREEDOM PARTY
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''

amk = '''
Chama cha Kisiasa -MAENDELEO DEMOCRATIC PARTY
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''
psk = '''
 
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 

'''
Mmwk = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Michael Njoroge Wainaina alikuwa mgombea Ward Mwakilishi wa Jamhuri ya Kenya kati ya 2013/02/08 na 2013/03/04 .Yeye amekuwa katika Muungano Mbunge wa Jubilee Alliance tangu 2013/02/13 Michael Njoroge Wainaina amekuwa Mwanachama wa National Rainbow Coalition tangu 2013 -02-08.
'''

jwk = '''JOSEPH WILLIAM NTHIGA NYAGAH
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''
mnk = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''
jkk = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''

sok = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''
pok = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''
nuk = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''
dmk = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 
'''
rnk = '''
Chama cha Kisiasa -INDEPENDENT CANDIDATE
Maelezo mengine kuhusu huyu mgombea rais yatapewa kwa muda usiokuwa mrefu.Tafadhali zidi kuangalia kila wakati kwa maelezo Zaidi. 

'''



