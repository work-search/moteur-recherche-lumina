import os

class Config:
    SECRET_KEY = ''
    SERVER_PORT = os.environ.get('SERVER_PORT', 5000)

