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
from models import mapVal as mv
from models import funkoS as fs
from models import funkoDrop as fd

from models import funkoMotivo as fm

# from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired, Email
tmp = []

class firestorCRUD():
  

  def readFunkos(self,idPartner):
    self.idPartner = idPartner
    

    try:
        # Check if ID was passed to URL query
        
        if idPartner:
            all_todos = [doc.to_dict() for doc in main.todo_funkos.document(self.idPartner).collection("Dfunkos").where(u'Stock', u'>', 0).stream()]
            listaF = list()
            cont = 1

            

            for f in all_todos:
    
              listaF.append(pd.funko(
                cont,
                f['id'],
                f['Numero'],
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

  def readFunkosMap(self,idFunko):
      self.idFunko = idFunko


      try:
          # Check if ID was passed to URL query

          if idFunko:
              all_todos = [doc.to_dict() for doc in main.todo_funkosDB.document(self.idFunko).collection("Tiendas").stream()]

              listaF = list()

              for f in all_todos:
                print(f['codT'])
              
                listaF.append(mv.mapVal(
                  f['nombreT'],
                  f['lat'],
                  f['lng'],
                  f['precio'],
                  f['codT']
                ))


              return listaF
          else:
              return listaF
      except Exception as e:
          return f"An Error Occured: {e}"

  def readFunkosS(self,idFunko):
    self.idFunko = idFunko
    try:
        # Check if ID was passed to URL query
        if idFunko:
            all_todos = [doc.to_dict() for doc in main.todo_funkosDB.stream()]
            listaF = list()
            for f in all_todos:
            
              listaF.append(fs.funkoS(
                f['id'],
                f['Nombre'],
                f['Linea'],
                f['Imagen']
              ))

              
            return all_todos
        else:
            return all_todos
    except Exception as e:
        return f"An Error Occured: {e}"


  def readFunkosLinea(self,idFunko):
    self.idFunko = idFunko
    try:
        # Check if ID was passed to URL query
        if idFunko:
            all_todos = [doc.to_dict() for doc in main.todo_funkosLinea.stream()]
            listaF = list()
            for f in all_todos:
              data = []
            # List subcollections in each doc
              lista = [doc.to_dict() for doc in main.todo_funkosLinea.document(f['nombre']).collection("serie").stream()]

              obj = fd.funkoDrop(f['nombre'])
              for a in lista:
                obj.serie.append(a['nombre'])
              listaF.append(obj)

            return listaF
        else:
            return listaF
    except Exception as e:
        return f"An Error Occured: {e}"
  def busquedaBasicaA(self,linea,numero,nombre,coleccion,motivo,idFunko):
    self.linea = linea
    self.numero = numero
    self.nombre = nombre
    self.idFunko = idFunko
    self.coleccion = coleccion
    self.motivo = motivo


    combinacion = linea[0] + numero
    print(combinacion)
    try:
        data = []

        # Check if ID was passed to URL query
        if idFunko:
            all_todos = [doc.to_dict() for doc in main.todo_funkosDB.where(u'Numero', u'==', int(numero)).where(u'Motivo', u'==', motivo).where(u'Coleccion', u'==', coleccion).where(u'Linea', u'==', linea).where(u'Nombre', u'>=', nombre).stream()]
            listaF = list()

            for f in all_todos:
            # List subcollections in each do
              print("safasff")
              data.append(f['id'])
              

            return data
        else:
            return data
    except Exception as e:
        return f"An Error Occured: {e}"

  def busquedaBasica(self,linea,numero,nombre,idFunko):
    self.linea = linea
    self.numero = numero
    self.nombre = nombre
    self.idFunko = idFunko

    combinacion = linea[0] + numero
    print(combinacion)
    try:
        data = []

        # Check if ID was passed to URL query
        if idFunko:
            all_todos = [doc.to_dict() for doc in main.todo_funkosDB.where(u'Numero', u'==', int(numero)).where(u'Linea', u'==', linea).where(u'Nombre', u'>=', nombre).stream()]
            listaF = list()

            for f in all_todos:
            # List subcollections in each do
              print("safasff")
              data.append(f['id'])
              

            return data
        else:
            return data
    except Exception as e:
        return f"An Error Occured: {e}"


  def readFunkosLineaBusqueda(self,idFunko):
    self.idFunko = idFunko
    try:
        data = []

        # Check if ID was passed to URL query
        if idFunko:
            all_todos = [doc.to_dict() for doc in main.todo_funkosLinea.stream()]
            listaF = list()

            for f in all_todos:
            # List subcollections in each do
              data.append(f['nombre'])
              

            return data
        else:
            return data
    except Exception as e:
        return f"An Error Occured: {e}"

  def readFunkosMotivo(self,idFunko):
    self.idFunko = idFunko
    try:
        # Check if ID was passed to URL query
        if idFunko:
            all_todos = [doc.to_dict() for doc in main.todo_funkosMotivo.stream()]
            listaF = list()
            for f in all_todos:
              obj = fm.funkoMotivo(f['nombre'])
              listaF.append(obj)

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

  def getLat(self,idPartner,idTienda):
    self.idPartner = idPartner
    self.idTienda = idTienda
    valor = main.todo_ref.document(self.idPartner).collection("Tienda").document(idTienda).get({u'lat'}) 
    bal = u'{}'.format(valor.to_dict()['lat'])
    return bal
  def getLng(self,idPartner,idTienda):
    self.idPartner = idPartner
    self.idTienda = idTienda
    valor = main.todo_ref.document(self.idPartner).collection("Tienda").document(idTienda).get({u'lng'}) 
    bal = u'{}'.format(valor.to_dict()['lng'])
    return bal