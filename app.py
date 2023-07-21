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

@app.route('/s1')
def serviceOne():
   return render_template('serviceOne.html')

@app.route('/s2')
def serviceTwo():
   return render_template('serviceTwo.html')

@app.route('/s3')
def serviceThree():
   return render_template('serviceThree.html')

@app.route('/portfolio')
def portfolio():
   return render_template('portfolioList.html')

@app.route('/portfolio/popup')
def portfolio_popup():
   return render_template('portfolio.html')

@app.route('/chart')
def chart():
   return render_template('chart.html')

@app.route('/api/temp')
def temp_data():
   data = ref.child('temp').get()
   return data   

@app.route('/api/list')
def ticker_list():
   data = ref.child('tickers').get()
   return data

@app.route('/api/pflist')
def ticker_pf_list():
   data = ref.child('tickers_pf').get()
   return data

@app.route('/api/select')
def select_list():
   try:
      data = ref.child('select').get()
   except:
      data = []
   return data

@app.route('/api')
def total_list():
    data = ref.child('data').get()
    print(len(data))
    return data

@app.route('/api/<string:ticker>')
def stock_data(ticker):
    data = ref.child('data').child(ticker).get()
    return data

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)