from flask import Flask, Response, request
from flask_cors import CORS
import xml.etree.ElementTree as ET
from Usuarios import *
from flask import jsonify
import xmltodict
import requests


app = Flask(__name__)


@app.route("/exml", methods=['POST'])
def parse_xml():
    # RECIBE EL PARAMETRO XML
    xml_data = request.data
    # ESCRIBE EL XML RECIBIDO
    archivo_xml = open("prueba_Desdefrontend.xml", "wb")
    archivo_xml.write(xml_data)

    # content_dict = xmltodict.parse(xml_data)
    # print(jsonify(content_dict))
    # return jsonify(content_dict)
    return ('exito')

    return Response(xml_data, mimetype='text/xml')



@app.route("/nxml", methods=['GET'])
def nombre_xml():

    import re


    data = open('prueba_Desdefrontend.xml', 'r+') 
    
    #Expresiones regulares
    fecha = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
    email= re.compile(r'([\w\.]+)@([\w\.]+)(\.[\w\.]+)')

    

    lineas = [str(i).rstrip('\n').strip() for i in data]
    
    # print(lineas)  

    separada_comas = []
    for x in lineas:
        separada_comas.append(x.strip().split(','))

    separada_dosPuntos = [] 
    for y in separada_comas:
        for m in y:
            separada_dosPuntos.append(m.split(':'))

    # print(separada_dosPuntos)



    #recuperacion de fechas 
    fechas = []

    for line in separada_dosPuntos:
        for z in line:
            res = re.search(fecha, z.strip())
            # print(res)
            if res:
                fechas.append(res.group(0))
            # elif res.string in fechas:
            #     fechas.pop(res.string)
                    
                # print(f"{res.string}\n")

    fechas_ordenadas = sorted(fechas) 

   
    
    fechas_noRepetidas = set(fechas_ordenadas)
    # print(fechas_noRepetidas)
    data.close

    
    
    # user = Usuario()
    lista_usuer = []


    
    banderaFecha = False
    banderaReportado = False
    banderaAfectados = False
    reportados = ""
    fechaUsuarios = ""
    afectados = ""

    contador = 0
    for user in separada_dosPuntos:
        
        contador += 1
        for use in user:
            validar_fecha = re.search(fecha, use.strip())
            if validar_fecha:
                banderaFecha = True
                fechaUsuarios += validar_fecha.group()
                contador = 0
            
            
            for email1 in user:
                validar_email = re.search(email, email1.strip())
                if  use == "Reportado por" and validar_email:
                    banderaReportado = True 
                    reportados += validar_email.group()
                    contador = 0
            
        if banderaReportado == True and banderaFecha == True and contador == 1:
          
            lista_usuer.append(Usuario(reportados,fechaUsuarios,afectados))
            banderaFecha = False
            banderaReportado = False
            banderaAfectados = False
            reportados = ""
            fechaUsuarios = ""
            afectados = ""

        lista_usuerr = set(lista_usuer)
        for ojo in lista_usuerr:
            print(ojo.reportado+ojo.fecha)
        #     if use == "Reportado por" and validar_email:
        #         banderaReportado = True 
        #         reportados += validar_email.group()
        #         break
        #     if validar_fecha:
        #         banderaFecha = True
        #         fechaUsuarios += validar_fecha.group()
        #     if  use == "Usuarios afectados" and validar_email:
        #         banderaAfectados = True
        #         afectados += validar_email.group()
        #     elif banderaFecha == True and banderaReportado ==True  and banderaAfectados == True:
        #         lista_usuer.append(Usuario(reportados,fechaUsuarios,afectados))
        #     reportados = ""
        #     fechaUsuarios = ""
        #     afectados = ""
        # pass
            
            


    # print(lista_usuer)
            

 

    
  
    f = open("resultado.xml", 'w')
    f.write('<Estadisticas>\n')
    f.write('<Estadtistica>\n')
    for fecha in fechas_noRepetidas:
        f.write('<Fecha>')
        f.write(fecha)
        f.write('</Fecha>\n')
    f.write('</Estadistica>\n')
  
    f.write('</Estadisticas>\n')
    f = open('resultado.xml', 'r+')

   
    return Response(response=f.readlines(),
                    mimetype='text/plain',
                    content_type='text/plain')































# cors = CORS(app, resources={r"/*": {"origin": "*"}})





# @app.route('/events/', methods=['POST'])
# def post_events():
#     data = open('data.txt', 'w+')
#     data.write(request.data.decode('utf-8'))
 
#     data.close()

#     return Response(response=request.data.decode('utf-8'),
#                     mimetype='text/plain',
#                     content_type='text/plain')


@app.route('/events/', methods=['GET'])
def get_events():
   
    import datetime
    import re
    data = open('prueba_Desdefrontend.xml', 'r+') 
    
    #Expresiones regulares
    fecha = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
    email= re.compile(r'([\w\.]+)@([\w\.]+)(\.[\w\.]+)')

    

    lineas = [str(i).rstrip('\n').strip() for i in data]
    
    # print(lineas)  

    separada_comas = []
    for x in lineas:
        separada_comas.append(x.strip().split(','))

    separada_dosPuntos = [] 
    for y in separada_comas:
        for m in y:
            separada_dosPuntos.append(m.split(':'))

    # print(separada_dosPuntos)



    #recuperacion de fechas 
    fechas = []

    for line in separada_dosPuntos:
        for z in line:
            res = re.search(fecha, z.strip())
            # print(res)
            if res:
                fechas.append(res.group(0))
            # elif res.string in fechas:
            #     fechas.pop(res.string)
                    
                # print(f"{res.string}\n")

    fechas_ordenadas = sorted(fechas) 

   
    
    fechas_noRepetidas = set(fechas_ordenadas)
    # print(fechas_noRepetidas)
    data.close

    
    
    # user = Usuario()
    lista_usuer = []


    
    banderaFecha = False
    banderaReportado = False
    banderaAfectados = False
    reportados = ""
    fechaUsuarios = ""
    afectados = ""

    contador = 0
    for user in separada_dosPuntos:
        
        contador += 1
        for use in user:
            validar_fecha = re.search(fecha, use.strip())
            if validar_fecha:
                banderaFecha = True
                fechaUsuarios += validar_fecha.group()
                contador = 0
            
            
            for email1 in user:
                validar_email = re.search(email, email1.strip())
                if  use == "Reportado por" and validar_email:
                    banderaReportado = True 
                    reportados += validar_email.group()
                    contador = 0
            
        if banderaReportado == True and banderaFecha == True and contador == 1:
          
            lista_usuer.append(Usuario(reportados,fechaUsuarios,afectados))
            banderaFecha = False
            banderaReportado = False
            banderaAfectados = False
            reportados = ""
            fechaUsuarios = ""
            afectados = ""

        lista_usuerr = set(lista_usuer)
        for ojo in lista_usuerr:
            print(ojo.reportado+ojo.fecha)
        #     if use == "Reportado por" and validar_email:
        #         banderaReportado = True 
        #         reportados += validar_email.group()
        #         break
        #     if validar_fecha:
        #         banderaFecha = True
        #         fechaUsuarios += validar_fecha.group()
        #     if  use == "Usuarios afectados" and validar_email:
        #         banderaAfectados = True
        #         afectados += validar_email.group()
        #     elif banderaFecha == True and banderaReportado ==True  and banderaAfectados == True:
        #         lista_usuer.append(Usuario(reportados,fechaUsuarios,afectados))
        #     reportados = ""
        #     fechaUsuarios = ""
        #     afectados = ""
        # pass
            
            


    # print(lista_usuer)
            

 

    
  
    f = open("resultado.xml", 'w')
    f.write('<Estadisticas>\n')
    f.write('<Estadtistica>\n')
    for fecha in fechas_noRepetidas:
        f.write('<Fecha>')
        f.write(fecha)
        f.write('</Fecha>\n')
    f.write('</Estadistica>\n')
  
    f.write('</Estadisticas>\n')
    f = open('resultado.xml', 'r+')

   
    return Response(response=f.readlines(),
                    mimetype='text/plain',
                    content_type='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
