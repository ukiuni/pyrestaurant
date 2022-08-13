from flask import Flask
from .database import init_db
from .config import Config
from . import models
# what is this session? I can run without this command
from flask_session import Session

def create_app():
    # creation of Object/instance of class Flask. this app is object for my flask class
    app = Flask(__name__)
    app.config.from_object(Config)
    # 
    app.secret_key = 'abc'

    # the function definition can be found in database.py
    # init_db(app) -> the app argument refers to your flask website where you want to start/use the database
    init_db(app)

    return app

# main app code. this app is just local variable
app = create_app()