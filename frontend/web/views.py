from django.shortcuts import render


# from web.models import textArea
# Create your views here.

#conexion entre apis 

endpoint = 'http://127.0.0.1:5000/' 

def index(request):
    return render(request, 'index.html')



def recuerarXML(request):

    if request.method == 'GET':
        pass