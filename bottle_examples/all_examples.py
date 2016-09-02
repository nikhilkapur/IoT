#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import bottle
import os

# Change working directory so relative paths (and template lookup) work again
# exec_path = os.path.dirname(__file__)
# if (exec_path):
#     os.chdir(exec_path)
os.chdir("/Users/nkapur/Documents/workspace/IoT/bottle_examples")

@bottle.route("/hello")
def hello():
    text = "Hello World"
    return text

@bottle.route("/url_params/<first_name>/<last_name>")
def url_params(first_name, last_name):
    text = "Hello %s, %s" % (last_name, first_name)
    return text

@bottle.route("/params")
def params():
    first_name = bottle.request.params.get("first_name")
    last_name = bottle.request.params.get("last_name")
    text = "Hello %s, %s" % (last_name, first_name)
    return text

@bottle.route("/template")
def template_simple():
    first_name = bottle.request.params.get("first_name")
    last_name = bottle.request.params.get("last_name")
    params = {}
    params['first_name'] = first_name
    params['last_name'] = last_name
    tmpl = bottle.template('simple.html', data=params)
    return tmpl

@bottle.route("/template_loop")
def template_loop():
    mylist = ['red', 'blue', 'yellow', 'green']
    tmpl = bottle.template('loop.html', colors=mylist)
    return tmpl

# If we run as WSGI/CGI, we have only one entry point
@bottle.route("/")
def index():
    text =  "Bottle!"
    command = bottle.request.params.get("command")
    #script = bottle.request.environ.get("SCRIPT_NAME")
    if command == 'hello':
        return hello()
    elif command == 'params':
        return params()
    elif command == 'template':
        return template_simple()
    elif command == 'template_loop':
        return template_loop()
    
    return text

# Run as stand-alone server
#bottle.run(host='0.0.0.0', port=8080) # Listen to HTTP requests on all interfaces

# Run as CGI script
bottle.run(server='cgi')

# Run as WSGI script
#application = bottle.default_app()

