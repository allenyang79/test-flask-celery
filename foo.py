from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask,current_app

foo = Flask(__name__)
foo.debug = True
@foo.route('/')
def foo_index():
    current_app.logger.info("foo")
    return 'foo_index'


