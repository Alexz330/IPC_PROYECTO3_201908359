from django.shortcuts import render, HttpResponse
import xml.etree.ElementTree as ET
import requests
import xmltodict

# Create your views here.

def index(request):
    global nom
    enxml = ""
    context={}
    if request.method == 'POST':
        archivo_subido= request.FILES['Cargar_archivo']
        nom=archivo_subido.name
        print(archivo_subido.name)
        cont = 0
        for linea in archivo_subido:
            if cont==0:
                l=str(linea[:len(linea)-2])
                cont=cont+1
            else:
                l = str(linea[1:])
                l = str(l[:len(linea) - 1])
            enxml=str(enxml)+str(l)+"\n"
        context['todoxml'] = enxml
       

        archivo_xml = open(nom, "r")
        lectura_xml = archivo_xml.read()
       

        r = requests.post('http://127.0.0.1:5000/exml',data=lectura_xml)
        
        # print(context)
        string_xml = r.content
        return render(request,'index.html',context)
    context2 = {}

    enxml1 = ""
    if request.method == "GET" :
        
        archivo_xmll = open("prueba1.xml", 'w')
        n = requests.get('http://127.0.0.1:5000/nxml')
        archivo_xmll.write(n.text)
        archivo_xmll.close()
        mostrarxml = open("prueba1.xml", 'r+')
        
        lineas = [str(i).rstrip('\n').strip() for i in mostrarxml]
        print(lineas)
        cont2 = 0
        for linea in lineas:
            if cont2==0:
                l=str(linea[:len(linea)-2])
                cont2=cont2+1
            else:
                l = str(linea[1:])
                l = str(l[:len(linea) - 1])
            enxml1=str(enxml1)+str(l)+"\n"
        context2['todoxml2'] = enxml1

        print()
        return render(request,'index.html',context2)
    
    
     



