from flask import Flask, Response, request
from flask_cors import CORS
import xml.etree.ElementTree as ET
from Usuarios import *
from flask import jsonify
from Estadistica import *


app = Flask(__name__)


@app.route("/mandarxml", methods=['POST'])
def parse_xml():
    xml_data = request.data
    
    archivo_xml = open("prueba_Desdefrontend.xml", "wb")
    archivo_xml.write(xml_data)

    

    return Response(xml_data, mimetype='text/xml')



@app.route("/obtenerxml", methods=['GET'])
def mandarFiltrado():

    import re

    linea=[]
    eventos=[]
    event = []
    afec=""
    eventosM=[] #Eventos modificados

    # Expresiones regulares
    expfecha = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
    expemail = re.compile(r'([\w\.]+)@([\w\.]+)(\.[\w\.]+)')
    experror=re.compile(r'([0-9]{5,5})')
    
    with open("prueba_Desdefrontend.xml", 'r') as archivo:
        lineas = archivo.read().splitlines()
        for l in lineas:  # Con este for leo el archivo
            n = l.replace("\t", "").replace("Guatemala,","")
            linea.append(n)
            if l == "\t</EVENTO>":
                eventos.append(linea)
                linea = []
            elif l == "<EVENTOS>":
                linea.pop()
        print(eventos)


        for x in range(len(eventos)):
            for y in range(len(eventos[x])):
                if y == 3:                                          
                    c = eventos[x][y].split(",")                    
                    for co in c:                                   
                        corr = re.search(expemail, co.strip())      
                        if corr:
                            afec = afec + "," + corr.group(0)      
                    afec=afec[1:]
                    event.append(afec)                             
                    afec=""
                else:
                    correo = re.search(expemail, eventos[x][y].strip())
                    fecha = re.search(expfecha, eventos[x][y].strip())
                    error = re.search(experror, eventos[x][y].strip())
                    if fecha:
                        event.append(fecha.group(0))
                    if correo:
                        event.append(correo.group(0))
                    if error:
                        event.append(error.group(0))
            print(event)
            eventosM.append(event)
            event=[]

        final=[]
        for a in range(len(eventosM)):
            final.append(Usuario(eventosM[a][0],eventosM[a][1],eventosM[a][2].split(","),eventosM[a][3]))
            #print(str(final[a].fecha) + str(final[a].afectados))

        fechas=[]
        for fe in range(len(final)):
            fechas.append(final[fe].fecha)
        fechas=sorted(list(set(fechas)))

        print(fechas)

        esta=[]
        testa=[]
        tempfinal=final
        cfechas=""
        cafect=""
        cerror=""

        for n in range(len(fechas)):
            esta.append(tempfinal[n].fecha)
            for m in range(len(final)):
                if tempfinal[m].fecha == fechas[n]:
                    cfechas = (cfechas + "," + tempfinal[m].correo).strip()
                    for a in tempfinal[m].afectados:
                        cafect = (cafect + "," + a).strip()
                    cerror = (cerror + "," + tempfinal[m].error).strip()
            cfechas = cfechas[1:]
            cafect = cafect[1:]
            cerror=cerror[1:]
            esta.append(cfechas)
            esta.append(cafect)
            esta.append(cerror)
            cfechas=""
            cafect=""
            cerror=""
            testa.append(esta)
            esta=[]

        print(testa)

        festadistica = []
        for a in range(len(testa)):
            festadistica.append(Estadistica(testa[a][0].strip(), testa[a][1].strip().split(","), testa[a][2].strip().split(","), testa[a][3].strip().split(",")))

        errores=[]


        cont=0
        f = open("estadisticas.xml", 'w')
        f.write('<ESTADISTICAS>\n')
        for k in range(len(festadistica)):
            f.write('\t<ESTADISTICA>\n')
            f.write('\t\t<FECHA>' + festadistica[k].fecha + '</FECHA>\n')
            f.write('\t\t<CANTIDAD_MENSAJES>' + str(len(festadistica[k].usuarios)) + '</CANTIDAD_MENSAJES>\n')
            f.write('\t\t<REPORTADO POR>\n')

            for u in festadistica[k].usuarios:
                f.write('\t\t\t<USUARIO>\n')
                f.write('\t\t\t\t<EMAIL>' + u+ '</EMAIL>\n')
                f.write('\t\t\t\t<CANTIDAD_MENSAJES>' + '1' + '</CANTIDAD_MENSAJES>\n')
                f.write('\t\t\t</USUARIO>\n')

            f.write('\t\t</REPORTADO POR>\n')
            f.write('\t\t<AFECTADOS>\n')

            for aff in festadistica[k].afectados:
                f.write('\t\t\t<AFECTADO>' + aff + '</AFECTADO>\n')

            f.write('\t\t</AFECTADOS>\n')
            f.write('\t\t<ERRORES>\n')
            f.write('\t\t\t<ERROR>\n')

            errores = sorted(list(set(festadistica[k].error)))
            for ax in range(len(errores)):
                for ay in range(len(festadistica[k].error)):
                    if errores[ax] == festadistica[k].error[ay]:
                        cont = cont + 1
                f.write('\t\t\t\t<CODIGO>' + errores[ax] + '</CODIGO>\n')
                f.write('\t\t\t\t<CANTIDAD_MENSAJES>' + str(cont) + '</CANTIDAD_MENSAJES>\n')
                cont=0

            f.write('\t\t\t</ERROR>\n')
            f.write('\t\t</ERRORES>\n')

            f.write('\t</ESTADISTICA>\n')
        f.write('</ESTADISTICAS>\n')

    f = open('estadisticas.xml', 'r+')
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
