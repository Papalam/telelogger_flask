from flask import request, jsonify
from werkzeug.utils import redirect

from services import Telegram
from telebot import app


@app.route('/', methods=['GET', 'POST'])
def show_root():
    if request.method == 'GET':
        return redirect('http://kremlin.ru')
    handler = Telegram.create()
    try:
        result = handler.send_message()
    except Exception as ex:
        result = {'error': ex.args[0]}
    return jsonify(result)
