from django.http import HttpResponse

def greeting(request): #View
    return HttpResponse("Salu2 a to2")

def pedro(request):
    return HttpResponse("Tojo")