from flask import Flask
import database
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/txhash/<code>/<tx>')
def hello_worldo(code, tx):
    database.Extend.update(code, tx)
    return 'Hello, World!'

