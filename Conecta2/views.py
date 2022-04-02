from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
from django.shortcuts import render
import datetime

class Persona(object):
    def __init__(self, nombre, apellido):
        self.nombre=nombre
        self.apellido=apellido

def greeting(request): #View
    return HttpResponse("Salu2 a to2")

def pedro(request): #Second view
    document = "<html><body><h1>TojoOoOOOOooOoOoO</h1></body></html>"
    return HttpResponse(document)

def date(request):

    persona1=Persona("Pedrito", "Samas")
    
    nombre="Juan"
    temasCurso=["Plantillas","Modelos","Formularios","Vistas","Despliegue"]

    #actual_date = datetime.datetime.now()
    
    #doc_externo=open("/Users/soportecda/Desktop/Proyecto Modular/Django/Conecta2/Conecta2/templates/template.html")
    #plt=Template(doc_externo.read())
    #doc_externo.close()

    #doc_externo=loader.get_template('template.html')

    #ctx=Context({"nombre_persona":persona1.nombre, "actualDate":actual_date, "temas":temasCurso})

    #document=doc_externo.render({"nombre_persona":persona1.nombre, "actualDate":actual_date, "temas":temasCurso})


    #return HttpResponse(document)

    #return render(request, "template.html", {"nombre_persona":persona1.nombre, "actualDate":actual_date, "temas":temasCurso})
    return render(request, "template.html", {"nombre_persona":persona1.nombre})

def ageCalculator(request, age, year): #Función calculadora de edad en cierto año..
    #ageActual = 18
    period = year-2022
    futureAge = age+period
    document = document = '''<html>
    <body>
    <h2>
    En el año %s tendras %s años
    </h2>
    </body>
    </html>''' %(year, futureAge)

    return HttpResponse(document)


def herence(request):
    actual_date = datetime.datetime.now()

    return render(request, "herence.html", {"actualDate":actual_date})


def herenceCss(request):
    #actual_date = datetime.datetime.now()

    return render(request, "herenceCss.html")
    #return render(request, "herenceCss.html", {"actualDate":actual_date})
