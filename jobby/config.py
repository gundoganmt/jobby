import psycopg2, os

class Config:
    SECRET_KEY = 'thisissecret'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:WulIgtM5zk@localhost/jobby"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "mahmut@jobby.net"
    MAIL_PASSWORD = "WulIgtM5zk"
