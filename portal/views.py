from . import portal
from utilities import response
from flask import request, jsonify


"""
Two routes - 
    Submitting article requests.
    List of articles requested.
    Sumbitting articles
"""
@portal.route('/request/', methods = ['POST'])
def submit_request():
    article =request.get_json()['title']
    print(article)
    result = {
        'result' : 'Successfully made article request!'
    }
    r = response(result, 200);
    r.headers['Access-Control-Allow-Origin'] =  ['*']
    return r

@portal.route('/list/', methods = ['GET'])
def list_requests():
    pass
    
@portal.route('/submit/', methods = ['POST'])
def submit_article():
    pass