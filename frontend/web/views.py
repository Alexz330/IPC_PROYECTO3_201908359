from django.shortcuts import render, HttpResponse
import xml.etree.ElementTree as ET
import requests
import xmltodict

# Create your views here.



def index(request):
    return render(request,'index.html')

def mostrarxml(request):
     if request.method == "POST":
        enxml = ""
        context={}
        archivo_subido= request.FILES['Cargar_archivo']
        nom=archivo_subido.name
        xml = open(nom,"r")
        print(archivo_subido.name)
        cont = 0
        for linea in xml:
           
            enxml=str(enxml)+str(linea)
        context['todoxml'] = enxml
       

        archivo_xml = open(nom, "r")
        lectura_xml = archivo_xml.read()
       

        r = requests.post('http://127.0.0.1:5000/mandarxml',data=lectura_xml)
        
        
        return render(request,'index.html',context)
    
def mostrariformacion(request):
    context2 = {}
    if request.method == "GET":    

        enxml1 = ""
        archivo_xmll = open("prueba1.xml", 'w')
        n = requests.get('http://127.0.0.1:5000/obtenerxml')
        archivo_xmll.write(n.text)
        archivo_xmll.close()

        mostrarxml = open("prueba1.xml", 'r')
        
        # lineas = [str(i).rstrip('\n').strip() for i in mostrarxml]
        # print(lineas)
        cont2 = 0
        for linea in mostrarxml:
          
            enxml1=str(enxml1)+str(linea)
        context2['todoxml2'] = enxml1

    return render(request,'index.html',context2)
    
