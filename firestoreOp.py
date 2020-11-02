from flask import Flask, render_template, redirect, url_for, request
import pyrebase
import requests
from firebase_admin import credentials, firestore, initialize_app
import json
from urllib3.exceptions import HTTPError as BaseHTTPError
import os
import tempfile
import json
from flask import Flask, request, jsonify
import app as main
from models import funko as pd
# from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired, Email
tmp = []

class firestorCRUD():
  

  def readFunkos(self,idPartner):
    self.idPartner = idPartner
    

    try:
        # Check if ID was passed to URL query
        
        if idPartner:
            all_todos = [doc.to_dict() for doc in main.todo_funkos.document(self.idPartner).collection("Dfunkos").stream()]
            listaF = list()
            cont = 1

            

            for f in all_todos:
    
              listaF.append(pd.funko(
                cont,
                f['id'],
                f['Num. Funko'],
                f['Nombre'],
                f['Linea'],
                f['Coleccion'],
                f['Serie'],
                f['Exclusivo'],
                f['Motivo'],
                f['Precio'],
                f['Stock'],
                f['Imagen']
              ))
              cont += 1

            
            return listaF
        else:
            return listaF
    except Exception as e:
        return f"An Error Occured: {e}"


  def print(self,lista):
    self.lista = lista
    
    for i in self.lista:
      print(i.id)
      print(i.nombre)
      print(i.linea)
      print("---------------")

  def delete(self,idPartner,id):
    self.idPartner = idPartner
    self.id = id
    print("EL id es:",id)
    main.todo_funkos.document(self.idPartner).collection("Dfunkos").document(id).delete()

