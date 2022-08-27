from unicodedata import category
from django.http.response import JsonResponse
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import  Card, User, Like
import json

#Suggestion math
import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import re

# Create your views here.


class SuggestionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user):
        #data = {'message': 'Success', 'cards': 'Cards'}
        #return JsonResponse(data)
        user = User.objects.get(id=id_user)
        cards = list(User.objects.values())

        if len(cards) > 0:
            data = {'message': 'Success', 'cards': cards}
        else:
            data = {'message': 'Cards not found...'}
        return JsonResponse(data)

    def post(self, request):
        card = json.loads(request.body)
        user = User.objects.get(id=card['id_user'])
        category = Category.objects.get(id=card['id_category'])
        CardPost.objects.create(
            content=card['content'], user=user, category=category)
        data = {'message': "Success"}

        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass

def Suggestion(request, idUser):
    # -*- coding: utf-8 -*-
    """
    Spyder Editor

    This is a temporary script file.
    """



    #!wget -O moviedataset.zip https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/moviedataset.zip
    print('unziping ...')
    #!unzip -o -j moviedataset.zip

    #Guardando la información de la película dentro de un dataframe de panda
    movies_df = pd.read_csv('movies.csv')

    #Guardando información del usuario dentro de un dataframe de panda
    ratings_df = pd.read_csv('ratings.csv')


    #Utilizar expresiones regulares para encontrar un año guardado entre paréntesis
    #Especificamos los paréntesis de forma tal de que no haya problemas con las películas que tiene el año en sus títulos
    #movies_df['year'] = movies_df.title.str.extract('(<img alt="\d\d\d\d" title="Rendered by QuickLaTeX.com" height="2" width="3" style="vertical-align: -4px;" data-src="https://www.statdeveloper.com/wp-content/ql-cache/quicklatex.com-6bed55770ce78fa33f73530474cdaed1_l3.png" class="ql-img-inline-formula quicklatex-auto-format lazyload td-animation-stack-type0-1" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="><noscript><img   alt="\d\d\d\d" title="Rendered by QuickLaTeX.com" height="2" width="3" style="vertical-align: -4px;" data-src="https://www.statdeveloper.com/wp-content/ql-cache/quicklatex.com-6bed55770ce78fa33f73530474cdaed1_l3.png" class="ql-img-inline-formula quicklatex-auto-format lazyload" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" /><noscript><img src="https://www.statdeveloper.com/wp-content/ql-cache/quicklatex.com-6bed55770ce78fa33f73530474cdaed1_l3.png" class="ql-img-inline-formula quicklatex-auto-format" alt="\d\d\d\d" title="Rendered by QuickLaTeX.com" height="2" width="3" style="vertical-align: -4px;"/></noscript>)',expand=False)
    movies_df['year'] = movies_df.title.str.extract(r'(\(\d+\))$', expand=False)

    #Sacando los paréntesis
    #movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)',expand=False)
    movies_df['year'] = movies_df.year.str.extract(r'(\d+)', expand=False)

    #Sacando los años de la columna 'title'
    #movies_df['title'] = movies_df.title.str.replace('(<img alt="\d\d\d\d" title="Rendered by QuickLaTeX.com" height="2" width="3" style="vertical-align: -4px;" data-src="https://www.statdeveloper.com/wp-content/ql-cache/quicklatex.com-6bed55770ce78fa33f73530474cdaed1_l3.png" class="ql-img-inline-formula quicklatex-auto-format lazyload td-animation-stack-type0-1" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="><noscript><img   alt="\d\d\d\d" title="Rendered by QuickLaTeX.com" height="2" width="3" style="vertical-align: -4px;" data-src="https://www.statdeveloper.com/wp-content/ql-cache/quicklatex.com-6bed55770ce78fa33f73530474cdaed1_l3.png" class="ql-img-inline-formula quicklatex-auto-format lazyload" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" /><noscript><img src="https://www.statdeveloper.com/wp-content/ql-cache/quicklatex.com-6bed55770ce78fa33f73530474cdaed1_l3.png" class="ql-img-inline-formula quicklatex-auto-format" alt="\d\d\d\d" title="Rendered by QuickLaTeX.com" height="2" width="3" style="vertical-align: -4px;"/></noscript>)', '')
    movies_df.title = movies_df.title.str.replace(r'(\(\d+\))$','')

    #Aplicando la función strip para sacar los espacios finales que pudiera haber
    movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())

    #Eliminando la columna géneros
    movies_df = movies_df.drop('genres', 1)

    ratings_df = ratings_df.drop('timestamp', 1)

    userInput = [
                {'title':'Breakfast Club, The', 'rating':5},
                {'title':'Toy Story', 'rating':3.5},
                {'title':'Jumanji', 'rating':2},
                {'title':"Pulp Fiction", 'rating':5},
                {'title':'Akira', 'rating':4.5}
            ] 
    inputMovies = pd.DataFrame(userInput)
    inputMovies


    #Filtrar las películas por título
    inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]

    #Luego juntarlas para obtener el movieId. Implícitamente, lo está uniendo por título.
    inputMovies = pd.merge(inputId, inputMovies)

    #Eliminando información que no utilizaremos del dataframe de entrada
    inputMovies = inputMovies.drop('year', 1)

    #Dataframe de entrada final

    #Si una película que se agregó no se encuentra, entonces podría no estar en el dataframe 

    #original o podría estar escrito de otra forma, por favor revisar mayúscula o minúscula.
    inputMovies


    #Filtrando los usuarios que han visto las películas y guardándolas
    userSubset = ratings_df[ratings_df['movieId'].isin(inputMovies['movieId'].tolist())]
    userSubset.head()

    #Groupby crea varios dataframes donde todos tienen el mismo valor para la columna especificada como parámetro
    userSubsetGroup = userSubset.groupby(['userId'])

    #Ordenamiento de forma tal de que los usuarios con más películas en común tengan prioridad
    userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

    userSubsetGroup = userSubsetGroup[0:100]


    #Magia

    #Guardar la Correlación Pearson en un diccionario, donde la clave es el Id del usuario y el valor es el coeficiente
    pearsonCorrelationDict = {}

    #Para cada grupo de usuarios en nuestro subconjunto 
    for name, group in userSubsetGroup:

        #Comencemos ordenando el usuario actual y el ingresado de forma tal que los valores no se mezclen luego

        group = group.sort_values(by='movieId')

        inputMovies = inputMovies.sort_values(by='movieId')

        #Obtener el N para la fórmula
        nRatings = len(group)
        
        #Obtener los puntajes de revisión para las películas en común
        temp_df = inputMovies[inputMovies['movieId'].isin(group['movieId'].tolist())]
        
        #Guardarlas en una variable temporal con formato de lista para facilitar cálculos futuros
        tempRatingList = temp_df['rating'].tolist()

        #Pongamos también las revisiones de grupos de usuarios en una lista
        tempGroupList = group['rating'].tolist()

        #Calculemos la Correlación Pearson entre dos usuarios, x e y
        Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
        Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
        Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
    
        #Si el denominador es diferente a cero, entonces dividir, sino, la correlación es 0.
        if Sxx != 0 and Syy != 0:
            pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
        else:
            pearsonCorrelationDict[name] = 0

    pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
    pearsonDF.columns = ['similarityIndex']
    pearsonDF['userId'] = pearsonDF.index
    pearsonDF.index = range(len(pearsonDF))
    pearsonDF.head()

    topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
    topUsers.head()

    topUsersRating=topUsers.merge(ratings_df, left_on='userId', right_on='userId', how='inner')
    topUsersRating.head()

    #Se multiplica la similitud de los puntajes de los usuarios
    topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['rating']
    topUsersRating.head()

    #Se aplica una suma a los topUsers luego de agruparlos por userId
    tempTopUsersRating = topUsersRating.groupby('movieId').sum()[['similarityIndex','weightedRating']]
    tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
    tempTopUsersRating.head()

    #Se crea un dataframe vacío
    recommendation_df = pd.DataFrame()
    #Ahora se toma el promedio ponderado
    recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
    recommendation_df['movieId'] = tempTopUsersRating.index
    recommendation_df.head()

    recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
    recommendation_df.head(10)




