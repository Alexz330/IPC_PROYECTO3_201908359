from flask import Flask, Response, request
from flask_cors import CORS
import xml.etree.ElementTree as ET
from Usuarios import *

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})





@app.route('/events/', methods=['POST'])
def post_events():
    data = open('data.xml', 'w+')
    data.write(request.data.decode('utf-8'))
 
    data.close()

    return Response(response=request.data.decode('utf-8'),
                    mimetype='text/plain',
                    content_type='text/plain')


@app.route('/events/', methods=['GET'])
def get_events():
   
    import datetime
    import re
    data = open('data.xml', 'r+') 
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

    print(separada_dosPuntos)



    #recuperacion de fechas 
    fechas = []

    for line in separada_comas:
        for z in line:
            res = re.match(fecha, z.strip())
            # print(res)
            if res:
                fechas.append(res.group(0))
            # elif res.string in fechas:
            #     fechas.pop(res.string)
                    
                # print(f"{res.string}\n")
    fechas_ordenadas = sorted(fechas) 


    
    fechas_noRepetidas = set(fechas_ordenadas)

    data.close

    # user = Usuario()
    lista_usuer = []





    for usu in separada_dosPuntos:
        for a in usu:

            validar_email = re.match(email, a.strip())
            email1 = ""
            if  validar_email:  
                email1 += validar_email.group(0) 
            
            print(email1)
            email1 = ""


                

            # print(ree)
            # if ree: 
            #     lista_usuer.append(Usuario(lista_usuer.count(ree.string),ree.string))
                






    print(lista_usuer)

    # lineas = [str(i) for i in data]
    
    # for linea in lineas:
    #     print(linea)
   

    
   
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
