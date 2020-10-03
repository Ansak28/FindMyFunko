from flask import Flask, render_template, redirect, url_for, request
import pyrebase
import requests
from firebase_admin import credentials, firestore, initialize_app
import json
from urllib3.exceptions import HTTPError as BaseHTTPError

firebaseConfig = {
    "apiKey": "AIzaSyCFioub2_C5x-R9wkIzHaauobaGY3J2XZM",
    "authDomain": "findmyfunko-dfbb4.firebaseapp.com",
    "databaseURL": "https://findmyfunko-dfbb4.firebaseio.com",
    "projectId": "findmyfunko-dfbb4",
    "storageBucket": "findmyfunko-dfbb4.appspot.com",
    "messagingSenderId": "744537797515",
    "appId": "1:744537797515:web:f7569a93d78f34134f758e",
    "measurementId": "G-F5LEPKE8GX",
    "serviceAccount":"fbAdminConfig.json"
  }

app = Flask(__name__)

cred = credentials.Certificate('fbAdminConfig.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('usuarios')
todo_refUser = db.collection('usernames')



firebase =  pyrebase.initialize_app(firebaseConfig)
# dbFire= firestore.client()
# todo_ref = dbFire.collection('usuarios')
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        print(request.form['log'])

        if request.form['log'] == "log":
            username = request.form['username']
            password = request.form['password']

            
            if "@" in username:
                user = auth.sign_in_with_email_and_password(username,password)
                if user:
                    return redirect(url_for('home'))
                else:
                    print("invalid pass")
            else:
                if todo_refUser.document(username).get().exists:
                    val = todo_refUser.document(username).get({u'uid'})
                    bal = u'{}'.format(val.to_dict()['uid'])
                    print("hj: ",bal)
                    user = auth.sign_in_with_email_and_password(bal,password)
                    if user:
                        return redirect(url_for('home'))
                    else:
                        print("invalid pass")
                else:
                    print("noexiste")


        elif request.form['log'] == "reg":
            return redirect(url_for('signClient'))
        else:
            return redirect(url_for('signPartner'))
            
    return render_template('login_new.html')



@app.route('/signClient', methods=['GET', 'POST'])
def signClient():

    if request.method == 'POST':
        nombre = request.form['nombreC']
        apellidos = request.form['apellidosC']
        fNac = request.form['fNacC']
        phone = request.form['phoneC']
        mail = request.form['usernameC']

        data = {
            "nombre" : nombre, 
            "apellidos" : apellidos,
            "fNac" : fNac,
            "phone" :phone,
            "mail" :mail,
            "partner": 'false'
        }
        user = auth.create_user_with_email_and_password(mail,request.form['passwordC'])
        userId = user['localId']
        dataU = {
            "uid": mail
        }
        if user:
            todo_ref.document(userId[:100]).set(data)
            todo_refUser.document(nombre).set(dataU)
            return redirect(url_for('login'))
        else:
            print("invalid pass")  
    return render_template('createClient.html')



@app.route('/signPartner', methods=['GET', 'POST'])
def signPartner():

    
    if request.method == 'POST':

        nombre = request.form['nombre']
        fNac = request.form['fNac']
        dni = request.form['dni']
        mail = request.form['username']
        apellidos = request.form['apellidos']

        data = {
            "nombre" : nombre, 
            "apellidos" : apellidos,
            "fNac" : fNac,
            "dni" :dni,
            "mail" :mail,
            "partner": 'true'
        }


        try:
            print("Email already exists")
            user = auth.create_user_with_email_and_password(mail,request.form['password'])

            userId = user['idToken']
            todo_ref.document(userId[:100]).set(data)
            return redirect(url_for('login'))

        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            if error == "EMAIL_EXISTS":
                print("Email already exists")
                
        
    return render_template('createPartner.html')

@app.route('/home')
def home():    
    return "Correcto KKNERAZO" 

app.run(debug=True)