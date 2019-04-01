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

app = setup()

if __name__ == '__main__':
	app.run()