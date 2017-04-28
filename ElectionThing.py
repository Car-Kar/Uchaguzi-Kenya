from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

PAT = 'EAAarLkMVMy4BALcfghCBksMQuo5lqLMIsogY1OJEHxVDJZAdIR0KkKWqfdCEbbRIv7IeFrsTTEAFfNRo3y0vgFmZA7wCkcYsZAQSEwlBL6V5VZAexpR4LO4IB1hZAhaoDYejvT5hLjCeZCaiye8qCa5vNrOOGuSyAuWE5ZCZB5VMfwZDZD'
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
VoterRequirements = '''
The national elections are on Tuesday, August 8th.
You will need to have registered as a voter and carry your national identification, or passport to vote.
Please come out in support for our best future leaders.
'''

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
                if 'start' in MessageText.lower() or 'hello' in MessageText.lower() or 'hi' in MessageText.lower() or 'hey' in MessageText.lower():
                    SendMessage(SenderID, IntroductoryMessage)
                    SendMessage(SenderID, CountiesMessage)
                    SendMessage(SenderID, ContinueUsing)
                elif 'registration' in MessageText.lower():
                    SendMessage(SenderID, VoterRegistration)
                    SendMessage(SenderID, ContinueUsing)
                elif 'requirement' in MessageText.lower():
                    SendMessage(SenderID, VoterRequirements)
                    SendMessage(SenderID, ContinueUsing)
                elif 'governor' in MessageText.lower():
                    GovOptions(SenderID)
                elif 'senate' in MessageText.lower() or 'senator' in MessageText.lower():
                    SenOptions(SenderID)
                elif 'women' in MessageText.lower():
                    WomOptions(SenderID)
                elif 'president' in MessageText.lower():
                    names = Candidates(PresidentialCandidates)
                    TEXT = 'The presidential candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                elif 'uhuru' in MessageText.lower() or 'kenyatta' in MessageText.lower() or 'muigai' in MessageText.lower():
                    SendMessage(SenderID, uhuru)
                elif 'raila' in MessageText.lower() or 'amollo' in MessageText.lower() or 'odinga' in MessageText.lower():
                    SendMessage(SenderID, raila_info)
                    
                elif 'evans' in MessageText.lower() or 'kidero' in MessageText.lower():
                    SendMessage(SenderID, g_evans_info)
                    
                elif 'mike' in MessageText.lower() or 'sonko' in MessageText.lower():
                    SendMessage(SenderID, g_mike_info)
                    
                elif 'ali' in MessageText.lower() or 'joho' in MessageText.lower():
                    SendMessage(SenderID, g_ali_info)
                    
                elif 'mohamud' in MessageText.lower() or 'diba' in MessageText.lower():
                    SendMessage(SenderID, mohamud)
                    
                elif 'suleiman' in MessageText.lower() or 'shahbal' in MessageText.lower():
                    SendMessage(SenderID, g_suleiman_info)
                    
                elif 'hezron' in MessageText.lower() or 'awiti' in MessageText.lower():
                    SendMessage(SenderID, g_hezron_info)
                    
                elif 'jack' in MessageText.lower() or 'ragumba' in MessageText.lower():
                    SendMessage(SenderID, g_jack_info)
                    
                elif 'anyang' in MessageText.lower() or "nyong'o" in MessageText.lower():
                    SendMessage(SenderID, g_anyang_info)
                    
                elif 'chris' in MessageText.lower() or 'ondieki' in MessageText.lower():
                    SendMessage(SenderID, g_chris_info)
                    
                elif 'johnson' in MessageText.lower() or 'sakaia' in MessageText.lower():
                    SendMessage(SenderID, s_johnson_info)
                   
                elif 'richard' in MessageText.lower() or 'kavemba' in MessageText.lower():
                    SendMessage(SenderID, s_richard_info)
                    
                elif 'william' in MessageText.lower() or 'wahome' in MessageText.lower():
                    SendMessage(SenderID, s_william_info)
                    
                elif 'yasser' in MessageText.lower() or 'sheikh' in MessageText.lower():
                    SendMessage(SenderID, s_yasser_info)
                    
                elif 'mohammad' in MessageText.lower() or 'faki' in MessageText.lower():
                    SendMessage(SenderID, s_mohammad_info)
                    
                elif 'tendai' in MessageText.lower() or 'mtwana' in MessageText.lower():
                    SendMessage(SenderID, s_tendai_info)
                    
                elif 'millicent' in MessageText.lower() or 'abudho' in MessageText.lower():
                    SendMessage(SenderID, s_otieno_info)
                    
                elif 'otieno' in MessageText.lower() or 'odongo' in MessageText.lower():
                    SendMessage(SenderID, s_tendai_info)
                    
                elif 'rachel' in MessageText.lower() or 'shebesh' in MessageText.lower():
                    SendMessage(SenderID, w_rachel_info)
                    
                elif 'esther' in MessageText.lower() or 'passaris' in MessageText.lower():
                    SendMessage(SenderID, w_esther_info)
                    
                elif 'millicent' in MessageText.lower() or 'omanga' in MessageText.lower():
                    SendMessage(SenderID, w_millicent_info)
                    
                elif 'karen' in MessageText.lower() or 'nyamu' in MessageText.lower():
                    SendMessage(SenderID, w_karen_info)
                    
                elif 'sadaf' in MessageText.lower() or 'deen' in MessageText.lower():
                    SendMessage(SenderID, w_sadaf_info)
                   
                elif 'mishi' in MessageText.lower() or 'juma' in MessageText.lower():
                    SendMessage(SenderID, w_mishi_info)
                    
                elif 'tendai' in MessageText.lower() or 'mtwana' in MessageText.lower():
                    SendMessage(SenderID, s_tendai_info)
                    
                elif 'bye' in MessageText.lower():
                    SendMessage(SenderID, Goodbye)
                else: 
                    i = 0
                    if i <= 3:
                        SendMessage(SenderID, ApologyMessage)
                        i += 1
                    else:
                        SendMessage(SenderID, 'Please pick a valid option from the menu!')
                
            elif msg.get('postback'):
                i = 0
                PostbackText = msg['postback']['payload']
                if PostbackText == 'Get Started':
                    SendMessage(SenderID, IntroductoryMessage)
                elif PostbackText == 'presidential':
                    names = Candidates(PresidentialCandidates)
                    TEXT = 'The presidential candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                elif PostbackText == 'gubernatorial':
                    GovOptions(SenderID)
                elif PostbackText == 'senate':
                    SenOptions(SenderID)
                elif PostbackText == 'womrep':
                    WomOptions(SenderID)
                elif PostbackText == 'gnairobi':
                    names = Candidates(g_nairobi)
                    TEXT = 'The governor candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)
                elif PostbackText == 'gkisumu':
                    names = Candidates(g_kisumu)
                    TEXT = 'The governor candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)
                elif PostbackText == 'gmombasa':
                    names = Candidates(g_mombasa)
                    TEXT = 'The governor candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)
                elif PostbackText == 'smombasa':
                    names = Candidates(s_mombasa)
                    TEXT = 'The senate candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)
                elif PostbackText == 'snairobi':
                    names = Candidates(s_nairobi)
                    TEXT = 'The senate candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)
                elif PostbackText == 'skisumu':
                    names = Candidates(s_kisumu)
                    TEXT = 'The senate candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)
                elif PostbackText == 'wmombasa':
                    names = Candidates(w_mombasa)
                    TEXT = 'The women representative candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)
                elif PostbackText == 'wnairobi':
                    names = Candidates(w_nairobi)
                    TEXT = 'The women representative candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                    SendMessage(SenderID, CandidateMoreInfo)

                elif PostbackText == 'VoterReg':
                    SendMessage(SenderID, VoterRegistration)
                    SendMessage(SenderID, ContinueUsing)
                elif PostbackText == 'VoterReq':
                    SendMessage(SenderID, VoterRequirements)
                    SendMessage(SenderID, ContinueUsing)
                else:
                    while i <= 3:
                        SendMessage(SenderID, ApologyMessage)
                        i += 1
                    else:
                        SendMessage(SenderID, 'Please pick a valid option from the menu!')


                

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
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)


def GovOptions(RecipientID):
    print(('Sending county options to {0}').format(RecipientID))
    CountyText = 'From what county? Choose one below.'
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
                    'text': CountyText,
                    'buttons': [
                    {
                        'type' : 'postback',
                        'title' : 'Kisumu County',
                        'payload' : 'gkisumu'
                    },
                    {
                        'type' : 'postback',
                        'title' : 'Mombasa County',
                        'payload' : 'gmombasa'
                    },
                    {
                        'type' : 'postback',
                        'title' : 'Nairobi County',
                        'payload' : 'gnairobi'

                    }]
                }
            }
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages?access_token=' + PAT, headers = headers, data = data)
    if r.status_code != 200:
        print(r.text)

def SenOptions(RecipientID):
    print(('Sending county options to {0}').format(RecipientID))
    CountyText = 'From what county? Choose one below.'
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
                    'text': CountyText,
                    'buttons': [
                    {
                        'type' : 'postback',
                        'title' : 'Kisumu County',
                        'payload' : 'skisumu'
                    },
                    {
                        'type' : 'postback',
                        'title' : 'Mombasa County',
                        'payload' : 'smombasa'
                    },
                    {
                        'type' : 'postback',
                        'title' : 'Nairobi County',
                        'payload' : 'snairobi'

                    }]
                }
            }
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages?access_token=' + PAT, headers = headers, data = data)
    if r.status_code != 200:
        print(r.text)

def WomOptions(RecipientID):
    print(('Sending county options to {0}').format(RecipientID))
    CountyText = 'From what county? Choose one below.'
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
                    'text': CountyText,
                    'buttons': [
                    {
                        'type' : 'postback',
                        'title' : 'Mombasa County',
                        'payload' : 'wmombasa'
                    },
                    {
                        'type' : 'postback',
                        'title' : 'Nairobi County',
                        'payload' : 'wnairobi'

                    }]
                }
            }
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages?access_token=' + PAT, headers = headers, data = data)
    if r.status_code != 200:
        print(r.text)


def Candidates(Level):
    candidate = '\n'.join([str(cand) for cand in Level])
    return candidate



if __name__ == '__main__':
  app.run(port = 3000, debug = True)


#counties - Nairobi, Kiambu, Nakury, Mombasa, Kisumu
PresidentialCandidates = ['Uhuru Muigai Kenyatta - Jubilee', 'Raila Amollo Odinga - ODM(NASA)', 'Mohamud Diba - Independent Candidate']

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
g_mombasa = ['Ali Joho - ODM(NASA)', 'Suleiman Shahbal - Jubilee Alliance', 'Hezron Awiti - WIPER(NASA)']

g_ali_info = '''Hassan Joho is a Kenyan politician affiliated to the Orange Democratic Movement and was elected to represent the Kisauni Constituency in the National Assembly of Kenya during the Kenyan parliamentary election, 2007. On 4 March 2013, Joho was elected as the first governor of Mombasa County. Joho joined active politics in the year 2004, and became the Kisauni party chairman for the Liberal Democratic Party between 2006-2007. He was elected as Member of Parliament for Kisauni constituency and the Assistant Minister for Transport. On 4 March 2013 he was elected as Governor of Mombasa.'''
g_suleiman_info = '''Suleiman Shahbal was Managing Partner of GulfCap Investments Ltd until 2012 .He is Chief Executive and Director of Gulf African Bank and Bank Clerk of Citibank .Suleiman Shahbal is Secondary School Student of Nairobi School, Kenya He  is Founder & Executive Director of Trifoil Petroleu Ltd He is also Deputy General Manager of Bank of Muscat, UAE He has been Member of Wiper democratic Movement Kenya representing Mombasa since 2013-01 Suleiman Shahbal was Aspirant Governor of REPUBLIC OF KENYA representing Mombasa until 2013-03-04 Suleiman Shahbal has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-13.'''
g_hezron_info = '''Hezron Awiti was elected for the first time in Parliament in 2013 as the MP for Nyali Constituency in Mombasa County. He was elected on a Wiper Democratic Movement Party ticket in the CORD Coalition. He was blocked from running on ODM ticket after won the ODM ticket but was not denied the ticket because some people thought he stood no chance against a coastal candidate on other tickets. He won the seat with a convincing majority despite the fact that majority of the voters there were not Luo.Hezron Awiti has declared that he will challenge Mombasa Governor Hassan Joho for the gubernatorial seat in 2017 on a Wiper ticket.
'''
g_kisumu = ['Jack Ragumba - ODM(NASA)', "Peter Anyang' Nyong'o  - ODM(NASA)", 'Christopher Odieki - ODM(NASA)']




g_jack_info ='''Jack Nyanungo Ranguma, also known as JR, is a Kenyan politician and was the first Governor of Kisumu County, Kenya. Jack has a Master of Science (International Accounting and Management Information Systems) from the University of Illinois at Urbana-Champaign. Prior to entering politics Jack Ranguma had worked as an accountant for close to 30 years. In 2002 he was appointed Commissioner of Income Tax, and later Commissioner of Domestic Taxes, Kenya Revenue Authority. In 2008 he became Senior Policy Advisor, Tax Justice Network Africa, a pan-African organization.
'''
g_anyang_info = '''Peter Anyang' Nyong'o (born 10 October 1945) is a Kenyan politician. He is the Secretary General of the Orange Democratic Movement and was the acting party leader from March 11 until late May when Raila Odinga was in the United States and was elected to the National Assembly of Kenya in the December 2007 parliamentary election, representing the Kisumu Rural Constituency. He was the Minister for Medical Services and previously the Minister for Planning & National Development. He is currently serving as the Senator for Kisumu County.
'''

g_chris_info = '''Born in the Kisumu slums in 1983 went to a mixed public school to enjoy the Kenyan education system in a journey that culminated in his graduation in 2009 with a Bachelor of Architecture at the Jomo Kenyatta University of Agriculture and Technology. During his campus life he engaged student leadership and youth political movements and also in work study programs to support the siblings and joined business with like minded friends who were fellow students to start business and became pioneer agents for Safaricom mpesa business.
'''

s_nairobi = ['Johnson Sakaja - Jubilee', 'William Wahome - Jubilee', 'Richard Kavemba - Wiper Democratic Movement of Kenya']


s_johnson_info = '''Johnson Sakaja , the National Chairman of TNA is currently the Principal Partner at Arthur Johnson Consultants which offers financial and strategic advisory services to Governmental and Private business entities in Kenya. Sakaja Johnson studied Actuarial Science and is currently pursuing Political Economics where he found his interests lie.He began his foray into national politics through student politics at the University of Nairobi (NASA – as vice chair of the Actuarial Students Association and later in SONU).He has been involved in National Politics since the 2005 referendum and played a key role in the 2007 re-election of H.E. Mwai Kibaki. Sakaja was also instrumental in the constitution making process being a key consultant to the COE and Parliamentary Select Committee on the Constitution on the issue of Representation and helped formulate the formula for delimitation of electoral boundaries in Kenya.
'''

s_richard_info = '''Richard Mutinda Kavemba has been Member of Wiper democratic Movement of Kenya since 2013-02-15 
Richard Mutinda Kavemba was Aspirant Governor of REPUBLIC OF KENYA representing Nairobi between 2013-02-15 and 2013-03-04 
Richard Mutinda Kavemba has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-16'''

s_william_info = '''Businessman William Wahome has declared his interest to run for Nairobi senator. The businessman-cum-politician becomes one of the aspirants to announce a bid for the JP ticket..Wahome announced his bid at the home of Roysambu parliamentary aspirant Michael Karanja, where the two hosted their grassroots mobilisers.
'''

s_mombasa = ['Yasser Bajaber - FORD Kenya', 'Mohammad Faki - United Democratic Forum (UDF) Party', 'Tendai Mtwana - Independent Party']

s_yasser_info = '''Yasser Ali Sheikh has been Member of Ford Kenya since 2013-02-08 
Yasser Ali Sheikh was Aspirant MP of REPUBLIC OF KENYA representing Nyali between 2013-02-08 and 2013-03-04 
Yasser Ali Sheikh has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-13
'''


s_mohammad_info = '''
Mohamed Faki Mwinyihaji has been Member of United Democratic Forum Party (UDF) since 2013-02-08. 
Mohamed Faki Mwinyihaji has been Coalition Member of Amani (Peace) Coalition since 2013-02-13. 
Mohamed Faki Mwinyihaji was Aspirant MP of REPUBLIC OF KENYA representing Jomvu between 2013-02-08 and 2013-03-04.
'''
s_tendai_info = '''
Tendai Lewa Mtana has been Member of The Independent Party since 2013-02-08 
Tendai Lewa Mtana was Aspirant Governor of REPUBLIC OF KENYA representing Mombasa between 2013-02-08 and 2013-03-04 
Tendai Lewa Mtana has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-13
'''

s_nakuru = ['Susan Kihika - Jubilee',  'Jack Waihenya - Jubilee']
s_susan_info = '''
Susan Kihika, born in 1974, is the daughter of the late Nakuru veteran Politician Dickson Kihika Kimani who earned repute in the 1970s and 1980s. He is the only Kenyan to ever get elected as MP of three different constituencies(Nakuru North, Laikipia West and Molo). By Profession, Susan Kihika holds a Political Science and Government Degree from the University of North Texas in Denton, Texas, USA.She also did a Jurist Doctorate Law Degree from the Southern Methodist University in Dallas, Texas,USA. She was l elected the Vice Chairlady of the County Assemblies Forum, which is composed of all 47 County Assemblies in Kenya with a membership of over 2200 MCAs and 47 County Assembly speakers.Susan Kihika is well known for being involved in community projects and charity work including being involved in women groups projects across the county, advocating for rights and welfare of children particularly those living with disabilities and advancement of girl child education.
'''
s_jack_info = '''
A Nakuru Businessman and Engineer eyeing the Senatorial seat.
'''

s_kisumu = ['Otieno Odongo - ODM(NASA)', 'Milicent Abudho - ODM(NASA)']
s_otieno_info = '''
He was admitted to Maseno National School in 1964 through to 1967 where after O levels he proceeded to Friends School Kamusinga for  A levels in 1969. Thereafter in 1970 he was admitted to University of Nairobi for Civil Engineering Course graduating with Honours in 1973.He has a company: Engineering Consultancy Firm in the name of Otieno Odongo and Partners.
'''
s_milicent_info = '''
Milicent Anyango Abudho was Aspirant Women representative of REPUBLIC OF KENYA representing Kisumu between 2013-02-08 and 2013-03-04 
Milicent Anyango Abudho has been Member of The National Alliance (TNA) since 2013-02-08 
Milicent Anyango Abudho has been Coalition Member of Jubilee Alliance since 2013-02-13
'''

s_kiambu = ['Kimani Wamatanga - Jubilee', 'Karungo Thangwa - Jubilee']

s_kimani_info = '''2012 – 2013: St. Pauls University, Degree in Leadership and Management, 1980 – 1989 : Bombay University 2010 – 2012 :  C.E.O, King Group Limited.,2004 – 2012 : Managing Director, Auto Bass Limited.,2008  – 2012 : Director, Total Assurance,2008  – 2012 : Director, Kings Construction
'''
s_karungo_info = '''
Karungo wa Thang'wa is the Member of County Assembly for Ngewa in Kiambu. Karungo Paul Thangwa was Aspirant Ward Representative of REPUBLIC OF KENYA between 2013-02-08 and 2013-03-04 Karungo Paul Thangwa has been Member of The National Alliance (TNA) since 2013-02-08 Karungo Paul Thangwa has been Coalition Member of Jubilee Alliance since 2013-02-13.Karungo Paul Thangwa has been Ward Representative of REPUBLIC OF KENYA since 2013-03-10
'''

w_nairobi = ['Esther Passaris - CORD-ODM', 'Millicent Omanga - Jubilee', 'Rachel Shebesh', 'Karen Nyamu - Jubilee']
w_esther_info = '''Esther Muthoni Passaris OGW (born 20 October 1964) is a Kenyan social entrepreneur, philanthropist, and politician. A member of the Kenya National Congress, she has run for member of parliament for Embakasi Constituency as well as for women's representative for Nairobi County. She is regarded as one of the most well-known female public figures in Kenyan business and politics.
'''

w_rachel_info = '''Rachel is the UN Champion for disaster risk reduction in Africa, where her main role is to promote synergy between disaster risk reduction and climate change adaptation in Africa, and works closely with African parliamentarians to obtain political commitment to disaster risk reduction policies. Her current Political Position is as the 2013 Nairobi women representative. Rachel seems to mingle well the young people hence her supporters gave her the name Manzi wa Nai.
'''
w_millicent_info = '''
Millicent Omanga is a business woman married to one Dr Francis Nyambiobo with two children. Omanga wants to become the next Nairobi Women Representative.
'''
w_karen_info = '''
Karen Nyamu or “Bae wa Nai” (Nairobi's sweetheart) as she is commonly referred by her supporters is a children and women's lawyer, hence, her slogan Wakili wa Watoto na Wamama. 
'''


w_mombasa = ['Sadaf Deen - ODM(NASA)', 'Mishi Juma - ODM']

w_sadaf_info = '''
Sadaf Deen is currently the youngest aspirant for the Mombasa women rep position in Mombasa. She is 20 years old.'''
w_mishi_info = '''
Mishi actively participated in Likoni political campaigns in 1997 and 2002. She vied for Likoni parliamentary seat in 2007 and lost in party nominations which were marred by irregularities. She would like to see government funded drug rehabilitation centres established in Mombasa.
'''

raila_info = """Raila Amollo Odinga was born on January 7, 1945 in Maseno - the son of Vice President Jaramogi Oginga Odinga.
 He is running in the Orange Democratic Movement with Vice President Kalonzo Musyoka as his running mate. 
 Odinga has focused on youth in his campaign, promising to help them gain access to employment and education. 
 In 1997, Odinga lost a bid for the presidency. He served as minister of energy from 2001 to 2002 and as minister of roads, public works, andhousing from 2003 to 2005.
"""
uhuru = """Uhuru  Kenyatta was born in October 1961. 
He is the presidential candidate for the Jubilee Alliance. 
Kenyatta ran unsuccessfully for president in 2002, yet won a seat in parliament representing Gatundu South that same year. He ran for president again in 2007, but withdrew and put his support behind President Mwai Kibaki for re-election. Kibaki appointed Kenyatta minister for local governments in January 2008 before he became deputy prime minister and minister of trade in April 2008 as part of a coalition government deal to end the violence after the 2007 elections.
"""

mohamud = """Mohamud Abduba Dida was born in Kenya's Wajir District in 1975.
 A former teacher, Dida is competing for the presidency with the Alliancefor Real Change. His running mate is Joshua Odongo Onono, also a former teacher. Dida has vowed to be a president who focuses on the poor. 
 Dida has expressed confidence in his ability to do well in the elections, as he has said his party enjoys significant support among the youth. He holds a bachelor's degree in education from Kenyatta University and is currently pursuing a master's in religious studies from the University of Nairobi.
"""

