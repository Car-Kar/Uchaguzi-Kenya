from flask import make_response
import json

def response(data, status):
    response = make_response(json.dumps(data), status)
    response.headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
    return response
