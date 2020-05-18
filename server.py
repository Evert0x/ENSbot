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

@app.route("/txerror/<code>/<error>")
def err(code, error):
    if "insufficient funds" in error:
        database.Extend.error_(code, "insufficient funds")
    else:
        database.Extend.error_(code, "Error")

    return 'yes'
