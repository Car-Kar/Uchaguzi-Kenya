import sys
from bot import bot
from portal import portal
from flask import Flask
from flask_cors import CORS, cross_origin

def setup():
    application = Flask(__name__)
    application.register_blueprint(bot, url_prefix = '/messenger')
    application.register_blueprint(portal, url_prefix = '/portal')
    CORS(application)

    return application


if __name__ == '__main__':
    app = setup()
    app.config['private_key'] = sys.argv[1]
    app.run(port=5000, debug = True)
