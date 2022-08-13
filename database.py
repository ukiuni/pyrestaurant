from flask_sqlalchemy import SQLAlchemy
# from package import class
from flask_migrate import Migrate


db = SQLAlchemy()
# instance of SQLAlchemy class. object of my database SQLAlchemy the helper for my easy functions and commands.

# start the database in your application
def init_db(app):
    db.init_app(app)
    Migrate(app,db)
    # initializing the object that i created. app is in other .py file.