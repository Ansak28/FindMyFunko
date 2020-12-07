from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import pyrebase
import requests
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore, initialize_app
import json
from urllib3.exceptions import HTTPError as BaseHTTPError
import firestoreOp as fOP
import os
import tempfile
import json
from models import reservas as rv
# from flask_googlemaps import get_coordinates
from flask_googlemaps import GoogleMaps, Map
import googlemaps
from flask_session import Session

gmaps = googlemaps.Client(key='AIzaSyCM-1oaJiCMKdm5dWYQ61bHiCSA8Hsabww')
API_KEY = 'AIzaSyCM-1oaJiCMKdm5dWYQ61bHiCSA8Hsabww'
# from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired, Email
geocode_result = gmaps.geocode('calle cuenca 193 mayorazgo,15012, peru')
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
    "serviceAccount": "fbAdminConfig.json"
}

app = Flask(__name__)

app.secret_key = "12345"


app.config['GOOGLEMAPS_KEY'] = "AIzaSyCM-1oaJiCMKdm5dWYQ61bHiCSA8Hsabww"
GoogleMaps(app, key="AIzaSyCM-1oaJiCMKdm5dWYQ61bHiCSA8Hsabww")

cred = credentials.Certificate('fbAdminConfig.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('usuarios')
todo_refUser = db.collection('usernames')
todo_tiendas = db.collection('tiendasD')

todo_funkos = db.collection('funkos')
todo_funkosT = db.collection(u'funkos')
todo_funkosR = db.collection(u'funkosR')


todo_funkosDB = db.collection('funkosDB')
todo_funkosLinea = db.collection('linea')
todo_funkosMotivo = db.collection('motivo')
c = ""


firebase = pyrebase.initialize_app(firebaseConfig)
# dbFire= firestore.client()
# todo_ref = dbFire.collection('usuarios')
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def homee():
    # print ("La dir",geocode_result)
    # print ("La latitud es ",geocode_result[0]['geometry']['location']['lat'])
    # print ("La longitud es ",geocode_result[0]['geometry']['location']['lng'])

    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('primeraPantalla.html')


@app.route('/loginP', methods=['GET', 'POST'])
def loginP():


    return render_template('loginP.html')


@app.route('/reservasPartner/<userN>', methods=['GET', 'POST'])
def reservasP(userN):
    listaF = list()

    my_var = session.get('id', None)
    print(my_var)

    userNC = userN[3:]



    all_todos = [doc.to_dict() for doc in todo_funkosR.where(u'nombreT', u'==', userNC ).stream()]
    for f in all_todos:
        # if f['estado'] == "r" : 
        listaF.append(rv.reservas(
            f['imagen'],
            f['estado'],
            f['idFunko'],
            f['nombreT'],
            f['hora'],
            f['nombreC']
        ))

    
    # if request.method == 'POST':

    return render_template('reservas.html',userN = userN,  reservas=listaF)

@app.route('/<userN>/reservasCliente', methods=['GET', 'POST'])
def reservasCliente(userN):
    listaF = list()

    my_var = session.get('id', None)
    print(my_var)

    all_todos = [doc.to_dict() for doc in todo_funkosR.where(u'nombreC', u'==', userN ).stream()]


    for f in all_todos:
        # if f['estado'] == "r" : 
        listaF.append(rv.reservas(
            f['imagen'],
            f['estado'],
            f['idFunko'],
            f['nombreT'],
            f['hora'],
            f['nombreC']
        ))

    if request.method == 'POST':
        if request.form.get("ver"):

            nombre = request.form['nombreT']
            idFunko = request.form['idFunko']
            print(userN)
            return redirect(url_for('infoTienda', userN=userN, nombreT=nombre, idFunko=idFunko))
        if request.form.get("Cancelar"):
            print("sadf")
            nombre = request.form['nombreT']
            idFunko = request.form['idFunko']

            print(userN)
            print(nombre)
            print(idFunko)

            docs = todo_funkosR.where(u'nombreC', u'==', userN ).where(u'nombreT', u'==',nombre).where(u'idFunko', u'==',idFunko).stream()
            idTienda1 = ""
            idReesrva = ""
            for doc in docs:
                idReesrva = doc.id
                print(doc.id)
            todo_funkosR.document(idReesrva).delete()
            
            return redirect(url_for('reservasCliente', userN=userN, nombreT=nombre, idFunko=idFunko))
        # if request.form.get("estado"):
        #     print("entro")
        #     if request.form['dropD'] == 'Activos':
        #         listaF.clear()
        #         all_todos = [doc.to_dict() for doc in todo_funkosR.where(u'nombreC', u'==', userN ).stream()]
        #         listaF = filtros(all_todos,"r")

        #         return redirect(url_for('reservasCliente', userN=userN,listaFunko = listaF))

        #     if request.form['dropD'] == 'Vencidos':
        #         listaF.clear()

        #         all_todos = [doc.to_dict() for doc in todo_funkosR.where(u'nombreC', u'==', userN ).stream()]
        #         listaF = filtros(all_todos,"f")
        #         return redirect(url_for('reservasCliente', userN=userN,listaFunko = listaF))

        #     if request.form['dropD'] == 'Completos':
        #         listaF.clear()

        #         all_todos = [doc.to_dict() for doc in todo_funkosR.where(u'nombreC', u'==', userN ).stream()]
        #         listaF = filtros(all_todos,"c")

            

        #     return redirect(url_for('reservasCliente', userN=userN,listaFunko = listaF))

    return render_template('reservasCliente.html', username=userN, reservas=listaF)

def filtros(lista,valor):

    listaF = list()
    for f in lista:
        print(f['estado'])
        print(valor)

        if f['estado'] == valor : 
            listaF.append(rv.reservas(
            f['imagen'],
            f['estado'],
            f['idFunko'],
            f['nombreT'],
            f['hora'],
            f['nombreC']
        ))
    return listaF



@app.route('/<userN>/busquedaA', methods=['GET', 'POST'])
def bAvanzada(userN):
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = request.form['numero']
        linea = request.form['linea']
        coleccion = request.form['coleccion']
        valC = "as"
        if coleccion.isnumeric():
            valC = int(coleccion)
        else:
            valC = coleccion
        motivo = request.form['motivo']
        prod = fOP.firestorCRUD()
        resultados = prod.busquedaBasicaA(
            linea, numero, nombre, valC, motivo, 1)
        print("resultados", linea, "-", numero, "-", coleccion, "-", motivo)

        print(resultados)
        if not resultados:
            return redirect(url_for('nofunko'))
        else:
            search = resultados[0]
            return redirect(url_for('mostrarMapa', userN=userN, idFunko=search))

    return render_template('busq_adv.html')


@app.route('/<userN>/busqueda', methods=['GET', 'POST'])
def bBasico(userN):
    prod = fOP.firestorCRUD()
    lista = prod.readFunkosLineaBusqueda(1)
    data = []
    for x in lista:
        data.append({'nombre': x})
    with open('static/json/jsonF4.json', 'w') as outfile:
        json.dump(data, outfile)

    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = request.form['numero']
        linea = request.form['linea']
        prod = fOP.firestorCRUD()
        resultados = prod.busquedaBasica(linea, numero, nombre, 1)
        print("resultados", linea, "-", numero)

        print(resultados)
        if not resultados:
            return redirect(url_for('nofunko'))
        else:
            search = resultados[0]
            return redirect(url_for('mostrarMapa', userN=userN, idFunko=search))

    return render_template('busq_basic.html', linea=lista)


@app.route('/mensajes/<userN>', methods=['GET', 'POST'])
def mensajes(userN):
    return render_template('mensajesPartner.html', user=userN)


@app.route('/login', methods=['GET', 'POST'])
def login():

    # json_array = open('load.json',)
    # data = json.load(json_array)
    # for item in data:
    #     todo_funkosDB.document(item["id"]).set(item)

    # prod = fOP.firestorCRUD()
    # listaF = prod.readFunkos("sNYFunkitos")
    # prod.print(listaF)

    # all_todos = [doc.to_dict() for doc in todo_funkos.document("LkGLl07Zc8ImYN7xWvfv").collection("Dfunkos").stream()]

    # for f in all_todos:
    #     print(f['id'])

    now1 = datetime.now()
    dt_string1 = now1.strftime("%d/%m/%Y %H:%M:%S")
    dt_string1 = datetime.strptime(dt_string1, "%d/%m/%Y %H:%M:%S")
    docs = todo_funkosR.stream()
    listaF = list()
    print(2)      
    for doc in docs:
        

        horaReserva = '00:60:00'
        horaReserva = timedelta(hours=1)
        tiempoR = todo_funkosR.document(doc.id).get({u'hora'})
        tReserva = u'{}'.format(tiempoR.to_dict()['hora'])
        estadoR = todo_funkosR.document(doc.id).get({u'estado'})
        Restado = u'{}'.format(estadoR.to_dict()['estado'])
        idFunko = todo_funkosR.document(doc.id).get({u'idFunko'})
        codF = u'{}'.format(idFunko.to_dict()['idFunko'])
        nombreT = todo_funkosR.document(doc.id).get({u'nombreT'})
        idTienda = u'{}'.format(nombreT.to_dict()['nombreT'])

        tReserva = datetime.strptime(tReserva, "%d/%m/%Y %H:%M:%S")
        print(1)
        valorH = dt_string1- tReserva
        balEs = ""
        if valorH < horaReserva :
            print("132")
        else:
            if Restado == 'r':
                valorNt = todo_tiendas.where(u'nombre', u'==', idTienda).limit(1).get()
                idTienda1 = ""
                for d in valorNt:
                    idTienda1 = u'{}'.format(d.to_dict()['id'])
                todo_funkosR.document(doc.id).update({u'estado': u"f"})
                print(idTienda1)
                print(codF)

                stock = todo_funkos.document(idTienda1).collection("Dfunkos").document(codF).get({u'Stock'})
                stock = u'{}'.format(stock.to_dict()['Stock'])
                stock = int(stock)
                stock =  stock - 1
            

                todo_funkos.document(idTienda).collection("Dfunkos").document(codF).update({u'Stock': stock})
            else:
                pass
        print(doc.id)



    error = None

    if request.method == 'POST':

        print(request.form['log'])

        if request.form['log'] == "log":
            username = request.form['username']
            password = request.form['password']

            if "@" in username:
                try:
                    user = auth.sign_in_with_email_and_password(
                        username, password)

                    userId = user['localId']
                    session['id'] = userId
                    print(userId)
                    valor = todo_ref.document(userId[:100]).get({u'partner'})
                    bal = u'{}'.format(valor.to_dict()['partner'])
                    print("asf: ", bal)
                    objeto = "valor"
                    listTienda = todo_ref.document(
                        userId[:100]).collection('Tienda').limit(1).get()
                    for d in listTienda:
                        idTienda = u'{}'.format(d.to_dict()['id'])
                    print(objeto)
                    if bal == "true":
                        return redirect(url_for("inv", userN=idTienda))
                    else:
                        return redirect(url_for("home"))

                except:
                    error = "Usuario o contrasena incorrecta"

            else:
                if todo_refUser.document(username).get().exists:
                    val = todo_refUser.document(username).get({u'uid'})
                    bal = u'{}'.format(val.to_dict()['uid'])
                    print("hj: ", bal)
                    user = auth.sign_in_with_email_and_password(bal, password)
                    userId = user['localId']
                    session['id'] = userId
                    if user:
                        return redirect(url_for('home', userN=username))
                    else:
                        print("invalid pass")
                else:
                    print("noexiste")

        elif request.form['log'] == "reg":
            return redirect(url_for('signClient'))
        else:
            return redirect(url_for('signPartner'))

    return render_template('login_new.html', error=error)


@app.route('/signClient', methods=['GET', 'POST'])
def signClient():

    if request.method == 'POST':
        nombre = request.form['nombreC']
        apellidos = request.form['apellidosC']
        fNac = request.form['fNacC']
        phone = request.form['phoneC']
        mail = request.form['usernameC']

        data = {
            "nombre": nombre,
            "apellidos": apellidos,
            "fNac": fNac,
            "phone": phone,
            "mail": mail,
            "partner": 'false'
        }
        user = auth.create_user_with_email_and_password(
            mail, request.form['passwordC'])
        userId = user['localId']
        dataU = {
            "uid": mail
        }
        if user:
            todo_ref.document(userId[:100]).set(data)
            todo_refUser.document(nombre).set(dataU)
            return redirect(url_for('welcomeC', name=nombre))
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
        codPostal = request.form['codPostal']

        strR = dirTienda + ', ' + codPostal + ', peru'
        print("dirCompleta: ", strR)
        geocode_result = gmaps.geocode(strR)
        print(geocode_result)
        # picture = request.files['picture']

        # temp = tempfile.NamedTemporaryFile(delete=False)
        # picture.save(temp.name)

        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        try:
            # print("Email already exists")
            user = auth.create_user_with_email_and_password(
                mail, request.form['password'])

            userId = user['localId']
            strT = userId[:3] + nTienda

            data = {
                "nombre": nombre,
                "codT": strT,
                "apellidos": apellidos,
                "telefono": tel,
                "fNac": fNac,
                "dni": dni,
                "mail": mail,
                "partner": 'true'
            }

            todo_ref.document(userId[:100]).set(data)

            dataT = {
                "nombre": nTienda,
                "dir": dirTienda,
                "email": emailTienda,
                "telf": telfTienda,
                "codPostal": codPostal,
                "lat": lat,
                "lng": lng,
                "id": strT
            }
            todo_ref.document(userId[:100]).collection(
                "Tienda").document(userId[:3] + nTienda).set(dataT)
            todo_tiendas.document(userId[:3] + nTienda).set(dataT)
            # firebase.storage().put(temp.name)

    # Clean-up temp image
            # os.remove(temp.name)
            return redirect(url_for('welcomeP', name=nombre))

        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            if error == "EMAIL_EXISTS":
                print("Email already exists")

    return render_template('createPartner_New.html')


@app.route('/<userN>/home', methods=['GET', 'POST'])
def home(userN):
    prod = fOP.firestorCRUD()
    data = []

    listaF = prod.readFunkosS("1")
    with open('static/json/json.json', 'w') as outfile:
        json.dump(listaF, outfile)

    if request.method == 'POST':
        search = request.form['Buscador']
        print("el codigo es", search)
        session['search'] = search
        return redirect(url_for("mostrarMapa", userN=userN, idFunko=search))

    return render_template('LandingPage.html', rows=listaF, username=userN)


@app.route('/invPartner/<userN>', methods=['GET', 'POST'])
def inv(userN):
    error = None
    prod = fOP.firestorCRUD()
    nT = userN[3:]
    listaF = prod.readFunkos(userN)
    listaF2 = prod.readFunkosLinea("1")
    listaF3 = prod.readFunkosMotivo("1")

    data = []
    data2 = []
    for a in listaF2:
        # print(a.nombre)
        # print(a.serie)
        dataE = []

        for b in a.serie:
            dataE.append({'nombre': b})
        data.append({
            'nombre': a.nombre,
            'serie': dataE}
        )
    with open('static/json/jsonF2.json', 'w') as outfile:
        json.dump(data, outfile)

    for x in listaF3:
        data2.append({'nombre': x.nombre})

    with open('static/json/jsonF3.json', 'w') as outfile:
        json.dump(data2, outfile)

    if request.method == 'POST':
        if request.form.get("update"):
            id = request.form['id']
            precio = request.form['precio']
            stock = request.form['stock']
            todo_funkos.document(userN).collection(
                "Dfunkos").document(id).update({u'Precio': precio})
            todo_funkos.document(userN).collection(
                "Dfunkos").document(id).update({u'Stock': stock})
            return redirect(url_for("inv", userN=userN))

        if request.form.get("add"):
            # id = request.form['id']
            num = request.form['num']
            # nombre = request.form['nombre']
            linea = request.form['linea']
            coleccion = request.form['coleccion']
            # serie = request.form['serie']

            motivo = request.form['motivo']
            stock = request.form['stock']
            precio = request.form['precio']

            if motivo[0] == "-":
                motivo = "0"
            id = linea[0] + num + coleccion[0] + motivo[0]
            print("se genero id : ", id)

            bal1 = "vacio"
            valor3 = todo_funkosDB.document(id).get({u'Nombre'})
            print("el nombre es: ", valor3)
            if valor3.exists:
                bal1 = u'{}'.format(valor3.to_dict()['Nombre'])
            if bal1 != "vacio":
                data = {
                    "id": id,
                    "Numero": num,
                    "Exclusivo": 1,
                    "Nombre": bal1,
                    "Linea": linea,
                    "Coleccion": coleccion,
                    "Serie": 1,
                    "Motivo": motivo,
                    "Stock": int(stock),
                    "Precio": precio,
                    "Imagen": "img"

                }
                my_var = session.get('id', None)

                rLat = prod.getLat(my_var, userN)
                rLng = prod.getLng(my_var, userN)

                dataDB = {
                    "nombreT": nT,
                    "precio": precio,
                    "lat": rLat,
                    "lng": rLng,
                    "codT": userN
                }
                todo_funkos.document(userN).collection(
                    "Dfunkos").document(id).set(data)
                todo_funkosDB.document(id).collection(
                    "Tiendas").document(userN).set(dataDB)
                return redirect(url_for("inv", userN=userN))
            else:
                error = 'La combinacion redirecciona a un funko no existente'

        if request.form.get("delete"):
            id = request.form.get("id")
            prod = fOP.firestorCRUD()
            prod.delete(userN, id)
            return redirect(url_for("inv", userN=userN))

        if request.form.get("sout"):
            # auth.current_user = None
            # print(auth.get_account_info(user['idToken']))
            return redirect(url_for("login"))

    return render_template('basic-table.html', rows=listaF, nt=nT, error=error, user=userN)

# @app.route("/delete", methods=["POST"])
# def delete():
#     id = request.form.get("id")
#     prod = fOP.firestorCRUD()
#     prod.delete("LkGLl07Zc8ImYN7xWvfv",id)
#     return redirect(url_for("inv",userN = userN))


@app.route("/welcomeP/<name>", methods=['GET', 'POST'])
def welcomeP(name):
    us = name
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('WelcomePartner.html', nombre=us)


@app.route("/welcomeC/<name>", methods=['GET', 'POST'])
def welcomeC(name):
    us = name
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('WelcomeClient.html', nombre=us)


@app.route("/<userN>/map/<idFunko>'", methods=['GET', 'POST'])
def mostrarMapa(userN, idFunko):

    if request.method == 'POST':
        print("entro a post")
        my_var = idFunko
        nombre = request.form['codT']
        precio = request.form['precio']

        # valoD = todo_funkosDB.document(nombre).get({u'dir'})
        # balD = u'{}'.format(valoD.to_dict()['dir'])

        # print("El nombre es", nombre)
        return redirect(url_for('mostrarInfo', userN=userN, idFunko=my_var, nombre=nombre, precio=precio, funko=my_var))

    else:
        my_var = idFunko
        print("paso correwcto: ", my_var)
        prod = fOP.firestorCRUD()
        res = prod.readFunkosMap(my_var)
        valor = todo_funkosDB.document(my_var).get({u'Imagen'})
        bal = u'{}'.format(valor.to_dict()['Imagen'])
        print(res)
        data = []
        fLat = 0
        fLng = 0
        for doc in res:
            fLat = doc.lat
            fLng = doc.lng
            item = {"icon": 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                    'lat': doc.lat,
                    'lng': doc.lng,
                    'infobox':
                    '<style>' +
                        '.button {' +
                    'background-color: #4CAF50; ' +
                    'border: none;' +
                    'color: white;' +
                    'padding: 10px;' +
                    'text-align: center;' +
                    'text-decoration: none;' +
                    'display: inline-block;' +
                    'font-size: 10px;' +
                    'margin: 4px 2px;' +
                    'cursor: pointer;' +
                        '}' +

                        '.button1 {border-radius: 2px;}' +
                        'input {' +
                            'border: none;' +
                            'background: transparent;' +
                        '}' +
                        '</style>' +

                    '<div class="card">' +
                    '<img src="https://cdn.shopify.com/s/files/1/0057/8630/4600/files/white_180x.jpg?v=1587504232" alt="Avatar" style="width:100%">' +

                    '<div class="container">' +
                    '<form id="SS" method="POST">' +
                        '<h4><input type="text" name="nombre" value="'+doc.nombre+'"></h4>' +
                        '<h4><input type="text" style="display:none;" name="codT" value="'+doc.codT+'"></h4>' +
                        '<p>El precio es: <input type="text" name="precio" value="'+doc.precio+'"></p>' +
                        '<button type="submit" value="Submit" class="button button1">Reservar</button>' +
                    # '</form>'
                        '</form>'
                    '</div>' +
                    '</div>'

                    # "<h1>"+doc.nombre+"</h1>" +
                    # "<p>El precio es: " + doc.stock + "</p>"

                    }
            data.append(item)
        sndmap = Map(
            identifier="sndmap",
            style="height:100%;width:100%;margin:0;",
            lat=fLat,
            lng=fLng,
            markers=data
        )

        return render_template('MapLocation.html', username=userN, sndmap=sndmap, img=bal)


@app.route("/<userN>/infoFunko", methods=['GET', 'POST'])
def mostrarInfo(userN):

    my_var = session.get('id', None)

    idFunko = request.args['idFunko']

    nombre = request.args['nombre']
    precio = request.args['precio']
    precio = "Precio: S/." + precio
    codF = request.args['funko']

    valorIm = todo_funkosDB.document(codF).get({u'Imagen'})
    balIm = u'{}'.format(valorIm.to_dict()['Imagen'])
    valorN = todo_funkosDB.document(codF).get({u'Nombre'})
    balN = u'{}'.format(valorN.to_dict()['Nombre'])
    valorL = todo_funkosDB.document(codF).get({u'Linea'})
    balL = u'{}'.format(valorL.to_dict()['Linea'])
    balL = "Linea: " + balL
    valorC = todo_funkosDB.document(codF).get({u'Coleccion'})
    balC = u'{}'.format(valorC.to_dict()['Coleccion'])
    balC = "Coleccion: " + balC

    valorNt = todo_tiendas.document(nombre).get({u'nombre'})
    balNt = u'{}'.format(valorNt.to_dict()['nombre'])
    valorDir = todo_tiendas.document(nombre).get({u'dir'})
    balDir = u'{}'.format(valorDir.to_dict()['dir'])
    balDir = "Direccion: "+balDir
    valorE = todo_tiendas.document(nombre).get({u'email'})
    balE = u'{}'.format(valorE.to_dict()['email'])
    valorT = todo_tiendas.document(nombre).get({u'telf'})
    balT = u'{}'.format(valorT.to_dict()['telf'])
    balT = "Contacto: " + balT

    now1 = datetime.now()
    dt_string1 = now1.strftime("%d/%m/%Y %H:%M:%S")
    dt_string1 = datetime.strptime(dt_string1, "%d/%m/%Y %H:%M:%S")
    print(my_var)
    print(idFunko)

    balEs = "n"
    horaRestante = "nel"
    balH = 0
    btnR = ""
    print(balNt)
    print(userN)
    print(codF)

    cond = todo_funkosR.where(u'nombreC', u'==', userN).where(u'idFunko', u'==',codF).get()
    if len(list(cond)) > 0:
        # hora = todo_funkosR.where(u'nombreT', u'==',balNt).where(u'nombreC', u'==', userN ).stream()
        
        all_todos = [doc.to_dict() for doc in todo_funkosR.where(u'nombreC', u'==', userN ).where(u'idFunko', u'==',codF).stream()]
        balH = ""
        balTienda = ""
        balEs = ""

        for f in all_todos:
            balH = f["hora"]
            balTienda = f["nombreT"]
            balEs = f["estado"]

        print(balH)
        print(balTienda)

        print(balEs)
        # balH = u'{}'.format(hora.to_dict()['hora'])

        # tienda = todo_ref.document(my_var).collection(
        #     "reservas").document(codF).get({u'nombreT'})
        # balTienda = u'{}'.format(tienda.to_dict()['nombreT'])



        horaReserva = ""
        if balH != '':
            balH = datetime.strptime(balH, "%d/%m/%Y %H:%M:%S")
            horaReserva = '00:60:00'
            horaReserva = timedelta(hours=1)
            valorH = dt_string1- balH

            if valorH < horaReserva :
                horaRestante = horaReserva - valorH
            else:
                horaRestante = "Tiempo Finalizado"
                balEs = "f"
                docs = todo_funkosR.where(u'nombreT', u'==',balNt).where(u'nombreC', u'==', userN ).where(u'idFunko', u'==',codF).stream()
                idTienda1 = ""
                idReesrva = ""

                for doc in docs:
                    idReesrva = doc.id

                todo_funkosR.document(idReesrva).update({u'estado': u"f"})

        # estado = todo_ref.document(my_var).collection(
        #     "reservas").document(codF).get({u'estado'})
        # balEs = u'{}'.format(estado.to_dict()['estado'])

        print(balNt)
        if balTienda == balNt:
            btnR = "Reservado"
        else:

            btnR = "Reservado en tienda: " + balTienda

        print(btnR)
        # print(balEs)


            
        # print(horaRestante)

    if request.method == 'POST':

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        print(balEs)

        data = {
            "idFunko": codF,
            "nombreT": balNt,
            "imagen": balIm,
            "estado": "r",
            "hora": dt_string,
            "nombreC": userN
        }

        if balEs == "r":
            return redirect(url_for('mostrarInfo', userN=userN, idFunko=my_var, nombre=nombre, precio=precio, funko=idFunko))
        else:

            # todo_ref.document(my_var).collection(
            #     "reservas").document(idFunko).set(data)
            valorNt = todo_tiendas.where(u'nombre', u'==', balNt).limit(1).get()
            idTienda = ""
            for d in valorNt:
                idTienda = u'{}'.format(d.to_dict()['id'])
            cond1 = todo_funkosR.where(u'nombreC', u'==', userN).where(u'idFunko', u'==',codF).get()
            if len(list(cond1)) > 0:
                idReesrva = ''
                docs = todo_funkosR.where(u'nombreC', u'==', userN ).where(u'idFunko', u'==',codF).stream()
                for doc in docs:
                    idReesrva = doc.id
                todo_funkosR.document(idReesrva).set(data)

            stock = todo_funkos.document(idTienda).collection("Dfunkos").document(codF).get({u'Stock'})
            stock = u'{}'.format(stock.to_dict()['Stock'])
            stock = int(stock)
            stock =  stock - 1
            todo_funkosR.add(data)

            todo_funkos.document(idTienda).collection("Dfunkos").document(codF).update({u'Stock': stock})
            return redirect(url_for('mostrarInfo', userN=userN, idFunko=my_var, nombre=nombre, precio=precio, funko=idFunko))

    return render_template('FunkoLocated.html', username=userN, imagen=balIm, nombreT=balNt, precio=precio, nombreF=balN,
                           linea=balL, coleccion=balC, emailT=balE, telf=balT, dir=balDir, estado=balEs, hora=balH, btnR=btnR)


@app.route("/<userN>/infoTienda/<nombreT>'", methods=['GET', 'POST'])
def infoTienda(userN, nombreT):
    idFunko = request.args['idFunko']
    my_var = session.get('id', None)
    data = []
    fLat = 0
    fLng = 0
    
    balH = 0
    btnR = ""
    print(userN)
    print(my_var)
    cond = todo_funkosR.where(u'nombreT', u'==',nombreT).where(u'nombreC', u'==', userN).where(u'idFunko', u'==',idFunko).get()

    if len(list(cond)) > 0:
        
        all_todos = [doc.to_dict() for doc in todo_funkosR.where(u'nombreT', u'==',nombreT).where(u'nombreC', u'==', userN ).where(u'idFunko', u'==',idFunko).stream()]
        balH = ""


        for f in all_todos:
            balH = f["hora"]


        balH = datetime.strptime(balH, "%d/%m/%Y %H:%M:%S")
        print(balH)
        

    valorNt = todo_tiendas.where(u'nombre', u'==', nombreT).limit(1).get()
    for d in valorNt:
        fLat = u'{}'.format(d.to_dict()['lat'])
        fLng = u'{}'.format(d.to_dict()['lng'])
        direccion = "Direccion: " + u'{}'.format(d.to_dict()['dir']) 

    item = {"icon": 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': fLat,
                'lng': fLng,
                'infobox':""

                }
    data.append(item)
    sndmap = Map(
        identifier="sndmap",
        style="height:100%;width:100%;margin:0;",
        lat=fLat,
        lng=fLng,
        markers=data
    )

    return render_template('infoTienda.html', username=userN, sndmap=sndmap, nombreT = nombreT,hora=balH, dir = direccion)


if __name__ == "__main__":
    app.run(debug=True)
