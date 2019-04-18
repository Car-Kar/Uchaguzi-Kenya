from . import portal
from utilities import response, load_file
from flask import request, jsonify
from flask import current_app as app

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
    print(load_file(app.config.get('private_key')))
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
