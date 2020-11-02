from flask import Flask, render_template, redirect, url_for, request, jsonify
import pyrebase
import requests
from firebase_admin import credentials, firestore, initialize_app
import json
from urllib3.exceptions import HTTPError as BaseHTTPError
import firestoreOp as fOP
import os
import tempfile
import json
# from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired, Email


idTienda = ""

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
todo_funkos = db.collection('funkos')



firebase =  pyrebase.initialize_app(firebaseConfig)
# dbFire= firestore.client()
# todo_ref = dbFire.collection('usuarios')
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    


    # json_array = f
    # for item in json_array:
    #     todo_funkos.document("LkGLl07Zc8ImYN7xWvfv").collection("Dfunkos").document(item["id"]).set(item)

    prod = fOP.firestorCRUD()
    listaF = prod.readFunkos("LkGLl07Zc8ImYN7xWvfv")
    prod.print(listaF)

    # all_todos = [doc.to_dict() for doc in todo_funkos.document("LkGLl07Zc8ImYN7xWvfv").collection("Dfunkos").stream()]

    # for f in all_todos:
    #     print(f['id'])

    
    if request.method == 'POST':

        print(request.form['log'])

        if request.form['log'] == "log":
            username = request.form['username']
            password = request.form['password']

            
            if "@" in username:
                user = auth.sign_in_with_email_and_password(username,password)
                userId = user['localId']
                print(userId)
                valor = todo_ref.document(userId[:100]).get({u'partner'}) 
                bal = u'{}'.format(valor.to_dict()['partner'])
                print("asf: ",bal)
                objeto = "valor"
                listTienda = todo_ref.document(userId[:100]).collection('Tienda').limit(1).get()
                for d in listTienda:
                    idTienda = u'{}'.format(d.to_dict()['id'])
                print(objeto)
                if bal == "true":

                    return redirect(url_for("inv",userN = idTienda))

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
        apellidos = request.form['apellidos']
        fNac = request.form['fNac']
        dni = request.form['dni']
        mail = request.form['username']
        tel = request.form['telf']

        nTienda = request.form['nTienda']
        dirTienda = request.form['dirTienda']
        emailTienda = request.form['emailTienda']
        telfTienda = request.form['telfTienda']

        data = {
            "nombre" : nombre, 
            "apellidos" : apellidos,
            "telefono" : tel,
            "fNac" : fNac,
            "dni" :dni,
            "mail" :mail,
            "partner": 'true'
        }

        dataT = {
            "nombre" : nTienda, 
            "apellidos" : dirTienda,
            "telefono" : emailTienda,
            "fNac" : telfTienda,

        }


        # picture = request.files['picture']

        # temp = tempfile.NamedTemporaryFile(delete=False)
        # picture.save(temp.name)


        try:
            # print("Email already exists")
            user = auth.create_user_with_email_and_password(mail,request.form['password'])

            userId = user['localId']
            todo_ref.document(userId[:100]).set(data)
            todo_ref.document(userId[:100]).collection("Tienda").document(userId[:3] + nTienda).set(dataT)
            # firebase.storage().put(temp.name)

    # Clean-up temp image
            # os.remove(temp.name)
            return redirect(url_for('login'))

        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            if error == "EMAIL_EXISTS":
                print("Email already exists")
                
        
    return render_template('createPartner_New.html')

@app.route('/home')
def home():    
    return render_template('LandingPage.html')


@app.route('/invPartner/<userN>', methods=['GET','POST'])
def inv(userN):
    prod = fOP.firestorCRUD()
    listaF = prod.readFunkos(userN)
    if request.method == 'POST':
        if request.form.get("update"):
            id = request.form['id']
            precio = request.form['precio']
            stock = request.form['stock']
            todo_funkos.document(userN).collection("Dfunkos").document(id).update({u'Precio': precio})
            todo_funkos.document(userN).collection("Dfunkos").document(id).update({u'Stock': stock})
            return redirect(url_for("inv",userN = userN))

        if request.form.get("add"):
            id = request.form['id']
            num = request.form['num']
            nombre = request.form['nombre']
            linea = request.form['linea']
            coleccion = request.form['coleccion']
            serie = request.form['serie']
            motivo = request.form['motivo']
            stock = request.form['stock']
            precio = request.form['precio']
            exclusivo = request.form['exclusivo']


            data = {
                "id" : id, 
                "Num. Funko" : num,
                "Exclusivo" : exclusivo,
                "Nombre" : nombre,
                "Linea" : linea,
                "Coleccion" :coleccion,
                "Serie": serie,
                "Motivo": motivo,
                "Stock": stock,
                "Precio": precio,
                "Imagen": "img"

            }
            todo_funkos.document(userN).collection("Dfunkos").document(id).set(data)

            return redirect(url_for("inv",userN = userN))
        if request.form.get("delete"):
            id = request.form.get("id")
            prod = fOP.firestorCRUD()
            prod.delete(userN,id)
            return redirect(url_for("inv",userN = userN))
        

    return render_template('basic-table.html',rows = listaF)

# @app.route("/delete", methods=["POST"])
# def delete():
#     id = request.form.get("id")
#     prod = fOP.firestorCRUD()
#     prod.delete("LkGLl07Zc8ImYN7xWvfv",id)
#     return redirect(url_for("inv",userN = userN))


@app.route("/infoFunko")
def mostrarInfo():
    return render_template('FunkoLocated.html')

app.run(debug=True)