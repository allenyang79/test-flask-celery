from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask,current_app

#from frontend_app import application as frontend
#from backend_app import application as backend

bar = Flask(__name__)
bar.debug = True
@bar.route('/')
def bar_index():
    current_app.logger.info("bar")
    return 'bar_index'
