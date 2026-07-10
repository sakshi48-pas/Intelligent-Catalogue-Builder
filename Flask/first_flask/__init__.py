from flask import Flask
            # flask - the flask library and Flask - a class inside the Flask library
from first_flask.user.views import mod as user_module

def create_app():
    app = Flask(__name__)


            #first_flask → user → views.py
            # mod is blueprint and using as user module is just a name
    app.register_blueprint(user_module)
            #This connects your blueprint to the app
            # All routes in views.py will now work
    return app