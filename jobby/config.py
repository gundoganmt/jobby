import psycopg2, os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '7c6b7967-dcba-4796-a261-f36b028144e3'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:WulIgtM5zk@localhost/jobby"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "destek@jobby.net"
    MAIL_PASSWORD = "WulIgtM5zk"
