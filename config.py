"""Provide Config in Flask"""
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')

# if .env cannot be read, then python will load/open/read the Class DevelopmentConfig
class DevelopmentConfig:

    # Turn on debug mode in Flask
    DEBUG = True

    # Set SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/restaurant?charset=utf8'.format(**{
    #     'user': os.environ.get('MYSQL_USER', 'root'),
    #     'password': os.environ.get('MYSQL_PASSWORD', 'root'),
    #     'host': os.environ.get('DB_HOST', 'localhost'),
    # })
    #
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', 'root'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'dbname': os.environ.get('DB_NAME', 'restaurant'),
    })

    SQLALCHEMY_TRACK_MODIFICATIONS = False      #  Good luck charm
    SQLALCHEMY_ECHO = False                     #  Good luck charm


Config = DevelopmentConfig
