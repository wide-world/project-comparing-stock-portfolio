import firebase_admin

from firebase_admin import credentials
from firebase_admin import db

# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('./mykey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kis-project-29909-default-rtdb.firebaseio.com/'
})

ref = db.reference('data/' + 'P15436').delete()