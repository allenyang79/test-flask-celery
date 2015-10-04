import os,sys
import logging
import time
import random
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask,current_app,make_response

from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


#from frontend_app import application as frontend
#from backend_app import application as backend
from foo import foo
from bar import bar


CELERY_REDIS_HOST = "192.168.99.100"

app = Flask(__name__)
app.debug = True
app.config.update(
    CELERY_BROKER_URL='redis://{}:6379'.format(CELERY_REDIS_HOST),
    CELERY_RESULT_BACKEND='redis://{}:6379'.format(CELERY_REDIS_HOST),
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task()
def add(a, b):
    with app.test_request_context() as request:
        for i in range(0,a+b):
            print "sleep...",i
            time.sleep(0.1 )
        return a + b


@app.route('/')
def app_index():
    return "index"


@app.route('/run')
def app_run():
    result = add.delay(3,5) 
    return "add_run: {}".format(result.get()) 

@app.route('/timestamp')
def get_timestamp():
    return str(time.time()) 


class yrange:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            time.sleep(0.001)
            i = self.i
            self.i += 1
            return str(i) + ","
        else:
            raise StopIteration()

class Middleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):

        # ex00 ,default response =================================
        return self.app(environ,start_response) 

        # Build the response body possibly
        # using the supplied environ dictionary
        # ex01 ===========================
        response_body = '<h3>Request method: %s : %s  </h3>' % (environ['REQUEST_METHOD'],environ["PATH_INFO"])
        response_body += "<br/>".join([
            '%s: %s' % (key, value) for key, value in sorted(environ.items())
        ])
        # ex02 ===========================
        response_body = [
            'The Beggining\n',
            '*' * 30 + '\n',
            response_body,
            '*' * 30 + '\n',
            '\nThe End'
        ]
        content_length = sum([len(s) for s in response_body])

        

        # HTTP response code and message
        status = '200 OK'

        # HTTP headers expected by the client
        # They must be wrapped as a list of tupled pairs:
        # [(Header name, Header value)].
        response_headers = [
            #('Content-Type', 'text/html'),
            ('Content-Type', 'text/plain'),
            # ('Content-Length', str(len(response_body)))
            # ('Content-Length', str(content_length))
        ]

        # Send them to the server using the supplied function
        start_response(status, response_headers)

        # Return the response body. Notice it is wrapped
        # in a list although it could be any iterable.
        #return response_body

        # ex03 : return a iterator =========================
        x = iter(["*" for i in range(0,content_length)])
        return x 
        #print [x for x in yrange(content_length)]

        # ex03 : return as a stream =========================
        return yrange(content_length)

 

#app = Middleware(app)
mainApp = DispatcherMiddleware(app, {
    '/foo':     foo,
    '/bar':     bar
})



if __name__ == '__main__':
    run_simple('localhost', 5000, mainApp,
    use_reloader=True, use_debugger=True, use_evalex=True)

