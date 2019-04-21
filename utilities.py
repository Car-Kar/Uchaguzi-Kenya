from flask import make_response
import json
import logging
from cryptography.hazmat.backends import default_backend
import jwt
import time
import requests

formatter = '[%(asctime)-15s] %(levelname)s [%(filename)s.%(funcName)s#L%(lineno)d] - %(message)s'

logging.basicConfig(level = logging.DEBUG, format = formatter)

# Create logger instance
logger = logging.getLogger('api')

def response(data, status):
    response = make_response(json.dumps(data), status)
    response.headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
    return response


def load_file(path):
    cert = None
    try:
        with open(path, 'r') as store:
            cert = store.read()
            cert = cert.encode()
            store.close()
    except (IOError, OSError):
        logger.error("Could not open private key file. Please confirm the correct location.")
        cert = None
    return cert

def create_github_headers(path, id):
    secs = int(time.time())
    expiry = secs + (10 * 60)
    payload = {
        'iat' : secs,
        'exp' : expiry,
        'iss' : id
    }
    privkey = None
    cert = load_file(path)
    if cert:
        privkey = default_backend().load_pem_private_key(cert, None)
    else:
        return
    bearer = jwt.encode(payload, privkey, algorithm = 'RS256')

    headers = {
        "Authorization" : "Bearer {}".format(bearer.decode()),
        "Accept" : "application/application/vnd.github.machine-man-preview+json"
    }
    return headers

def create_issue(title, label):
    
    
    
    

private_key = default_backend().load_pem_private_key(cert_bytes, None)

# Encode *anything* using the requires RS256 algorithm
test_jwt = jwt.encode({'some': 'payload'}, private_key, algorithm='RS256')
