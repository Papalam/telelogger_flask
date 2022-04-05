import logging
from logging.config import dictConfig

from flask import Flask

from config import LOGGING


dictConfig(LOGGING)

app = Flask(__name__)
app.logger = logging.getLogger('telebot_flask')
app.logger.debug('App starting')


