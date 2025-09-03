import os

class Config:
    SECRET_KEY = 'fdhfjsjlwww254'
    SERVER_PORT = os.environ.get('SERVER_PORT', 5000)
