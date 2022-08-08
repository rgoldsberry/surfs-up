from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1> Hello World </h1>'

@app.route('/FAQ')
def FAQ():
    return "You shouldn't have any questions"