import firebase_admin

from flask import Flask, render_template
from flask_cors import CORS
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)
CORS(app)

# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('./mykey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kis-project-29909-default-rtdb.firebaseio.com/'
})

ref = db.reference()

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/create')
def create():
   return render_template('create.html')

@app.route('/list')
def stock_list():
   data = ref.child('tickers').get()
   return data

@app.route('/api/<string:ticker>')
def stock_data(ticker):
    data = ref.child('ohlcv').child(ticker).get()
    return data

@app.route('/chart')
def chart():
   return render_template('chart.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug = True)