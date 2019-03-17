from flask import Blueprint

bot = Blueprint('bot', __name__)

from . import views