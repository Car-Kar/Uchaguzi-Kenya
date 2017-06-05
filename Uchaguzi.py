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
        self.curs.execute("""SELECT running_mate,political_bio, image FROM governor_candidates WHERE UPPER(name) Like  UPPER('%s') && UPPER(county) Like UPPER('%s') """ % (value1,value2))
        result= self.curs.fetchall()
        for row in result:
            return row[0], row[1]

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
options = ['pres', 'gov', 'senate', 'womrep', 'vote', 'contact']
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
                        FindingUser(SenderID)
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
                    
                        if msg.get('message'):
                            if 'start' in UserSays.lower() or 'hey' in UserSays.lower() or 'hi' in UserSays.lower() or 'hello' in UserSays.lower():
                                ReusableOptions(SenderID, Start, 'Kiswahili', 'English')
                            if Kiswahili == True and 'swahili' in UserSays.lower():
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
                                'Kagua Serikali',
                                'Wasiliana na serikali ya kata yako')
                            if Kiswahili is not True and 'english' in UserSays.lower():
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
                                'Contact',
                                'Take a survey'
                                )

                            if Kiswahili == True and 'nipe' in UserSays.lower():
                                SendMessage(SenderID, VoterRequirements)
                            if Kiswahili == True and 'mawaidha' in UserSays.lower():
                                response = '''Nitakutumia alani ya kukukumbusha siku ya uchaguzi.
                                Unataka alani ya siku gani?'''
                                ReusableOptions(SenderID, response, 'A Week Before', 'Two Days Before')

                            if level == 'vote' and UserSays.lower() in racer.lower():
                                MDB.PresidentialRace(racer.capitalize())
                                SendMessage(SenderID, 'Thank you for voting!')
                                ReusableOptions(SenderID, 'Do you want to see the results, go back home, or say goodbye?', 'Results', 'Home')
                        
                        
                        

                            if Kiswahili is not True and 'a week' in UserSays.lower():
                                response = 'I will be messaging you a week before the elections as a reminder'
                                SendMessage(SenderID, response)
                                Home(SenderID, 'Go back to home?', 'Home')

                            if Kiswahili is not True and 'two days' in UserSays.lower():
                                response = 'I will be messaging you two days before the elections as a reminder'
                                SendMessage(SenderID, response)
                                Home(SenderID, 'Go back to home?', 'Home')

                        
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
                                'Contact',
                                'Take a survey'
                                )

                            elif 'bye' in UserSays.lower():
                                SendMessage(SenderID, Goodbye)

                            elif level == 'pres' and UserSays.lower() in cands.lower():
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
                                  'Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  'Home')
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
                                  'Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  'Home')

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
                                  'Home')
                                else:
                                    SendMessage(SenderID, bio)
                                    HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
                                 If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  'Home')
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
                                  'Home')
                                else:
                                    SendMessage(SenderID, bio)
                                    HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  'Home')
                            elif level == 'gov' and UserSays.lower() in cands.lower():
                                
                                query = '%' + UserSays.lower() + '%'
                                county = '%' + county + '%'
                                run, bio = SQL.governor_bio(query, county)
                                bio = str(bio)
                                if len(str(run)) < 1:
                                    if len(bio) > 640:
                                        bio, bios = CheckTextLength(bio)
                                        response = bio + '-'
                                        SendMessage(SenderID, response)
                                        SendMessage(SenderID, bios)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  'Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
                                 If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  'Home')
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
                                  'Home')
                                    else:
                                        SendMessage(SenderID, bio)
                                        HomeP(SenderID, ''''Do you want to know about another candidate, or go back to home?
If you want to know about another candidate, send me his or her name, otherwise click the button below to go home''',
                                  'Home')

                            elif level == 'vote' and UserSays.lower() in racer.lower():
                                print('Im')

                            elif Kiswahili is not True and 'gov' == level:
                                query = '%' + county + '%'
                                candidates = SQL.governors(query)
                                if len(candidates) > 640:
                                    first_names, second_names = CheckListLength(candidates)
                                    response = 'The gubernatorial candidatesfor ' + county + ' are: \n' + str(first_names[0:])
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
                            elif Kiswahili is not True and 'vote' in UserSays.lower():
                                SendMessage(SenderID, 'If the elections happened tomorrow, which presidential candidate would you vote for?')

                            elif level == 'contact' and county is not None:
                                contacts = countydict[county]
                                print(contacts)

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
                            if Kiswahili is not True and UserSays == 'voters':
                                SendMessage(SenderID, VoterRequirements )
                                SendMessage(SenderID, 'Here are some helpful graphics to help you.')
                            
                                SendAttachment(SenderID,'image', 'https://farm5.staticflickr.com/4248/34872766342_a66c0fa485_o_d.jpg')
                                SendMessage(SenderID, ContinueUsing)
                                HomeP(SenderID, 'Go back to home, or do you want to say goodbye?', '\U000FE4B0 Home')

                            elif Kiswahili is not True and UserSays == 'poll':
                                ListTemplate(SenderID, 'Results', 'https://d30y9cdsu7xlg0.cloudfront.net/png/25759-200.png', 'See the results of the poll.' , '\\u1f5f3 Vote')

                            elif Kiswahili is not True and UserSays == 'registration':
                                SendAttachment(SenderID, 'image', 'https://farm5.staticflickr.com/4243/34193089344_55a2249bd6_o_d.jpg')
                                SendAttachment(SenderID, 'video', '')
                                SendMessage(SenderID, VoterRegistration)
                                HomeP(SenderID, 'Go back to home, or do you want to say goodbye?', '\U000FE4B0 Home')

                    
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

                            elif Kiswahili is not True and UserSays == 'gov':
                                CountyOptions(SenderID, 'From what county? Choose one below')

                            elif Kiswahili is not True and UserSays == 'senate':
                                CountyOptions(SenderID, 'From what county? Choose one below')
                            elif Kiswahili is not True and UserSays == 'womrep':
                                CountyOptions(SenderID, 'From what county? Choose one below')

                            elif Kiswahili is not True and UserSays == 'contact':
                                CountyOptions(SenderID, 'From what county? Choose one below')
                        

        



                            


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

def ListTemplate(RecipientID, TXT, A, B, C, D):

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        "recipient": {
        "id":"RECIPIENT_ID"
    },
    "message": {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "list",
            "top_element_style": "compact",
            "elements": [
                {
                    "title": A,
                    "image_url": B,
                    "subtitle": C,
                    "default_action": {
                        "type": "web_url",
                        "url": "https://uchaguzi-ke.herokuapp.com",
                        "messenger_extensions": true,
                        "webview_height_ratio": "tall",
                        "fallback_url": "https://uchaguzi-ke.herokuapp.com"
                    },             
                }
            ],
             "buttons": [
                {
                    "title": D,
                    "type": "postback",
                    "payload": "vote"                        
                }
            ]  
        }
    } 
    }})
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

def GenericTemplateOptions(RecipientID, A, B, C, D, E, F, G, H, I, J, K, L, M):
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
                        'payload' : 'contact',
                        'title' : L
                    } ,
                    {
                        'type' : 'postback',
                        'payload' : 'review',
                        'title' : M
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

