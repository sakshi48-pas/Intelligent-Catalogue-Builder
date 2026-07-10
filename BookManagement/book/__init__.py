from flask import Flask

def create_app():
    app = Flask(__name__)

    from book.views import mod
    app.register_blueprint(mod)

    return app