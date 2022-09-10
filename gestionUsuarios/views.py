from http.client import HTTPResponse
from unicodedata import category
from xml.etree.ElementTree import tostring
from django.http.response import JsonResponse
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Card as CardGU, User as UserGU, Like as LikeGU
from api.models import CardPost as Card, Category, User, Like, Save
from tqdm import tqdm
import json

# Suggestion math
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
        knn()
        dataFrame = Suggestion(id_user)
        if len(dataFrame) > 0:
            data = {'message': 'Success', 'cards': dataFrame}
        else:
            data = {'message': 'No cards to suggest'}
        return JsonResponse(data)

    def post(self, request):
        card = json.loads(request.body)
        user = User.objects.get(id=card['id_user'])
        category = Category.objects.get(id=card['id_category'])
        Card.objects.create(
            content=card['content'], user=user, category=category)
        data = {'message': "Success"}

        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


def Suggestion(idUser):
    print('unziping ...')

    #Guardando la información de las tarjetas y usuarios en un QuerySet
    #movies_df = pd.read_csv('movies.csv')
    cardList = list(Card.objects.values('id', 'user'))
    userList = list(User.objects.values('id'))
    likeList = list(Like.objects.values('id','user','card','status'))
    saveList = list(Save.objects.values('id','user','card','status'))

    #Comprobación de datos para iterar
    if len(cardList) <= 0 or len(userList) <= 0 or len(likeList) <= 0 or len(saveList) <= 0:
        data = {"message:": "Failure, no data found"}
        return JsonResponse(data)

    #Extrayendo las cards con like y saved del usuario a sugerir y guardado en un dataframe
    inputCardsLike = pd.DataFrame(Like.objects.filter(user=idUser).order_by('card').values('card'))
    inputCardsSave = pd.DataFrame(Save.objects.filter(user=idUser).order_by('card').values('card'))
    inputCardsLike.to_csv("inputCardsLike.csv")
    inputCardsSave.to_csv("inputCardsSave.csv")
    #Añadiendo un valor numérico si es saved o like
    inputCardsLike['rating'] = int(1)
    inputCardsSave['rating'] = int(2)
    #Guardado los datos del usuario con sus cards en input
    userInput = list()
    userInput = { }
    inputCards = pd.DataFrame(userInput)
    #Combinando las columnas de saved y like en una sumatoria
    inputCards = pd.merge_ordered(inputCardsLike,inputCardsSave,how='outer', left_on=['card'], right_on=['card']).sort_values('card')
    inputCards = inputCards.drop_duplicates()
    inputCards['rating_x'] = inputCards['rating_x'].fillna(0)
    inputCards['rating_y'] = inputCards['rating_y'].fillna(0)
    inputCards['rating'] = inputCards['rating_x'].astype(int) + inputCards['rating_y']
    inputCards = inputCards.drop(columns=['rating_x'])
    inputCards = inputCards.drop(columns=['rating_y'])
    #Guardando en CSV para respaldo.
    inputCards.to_csv('inputCards.csv')
    #inputCards = inputCards.head(20)

    #///////////////////////////////////////////////////
    #Guardado información de todas las cards con like y las guardadas en un dataframe, excluyendo las del usuario a sugerir
    ratingLike = pd.DataFrame(Like.objects.exclude(user=idUser).order_by('card').values('card','user'))
    ratingSave = pd.DataFrame(Save.objects.exclude(user=idUser).order_by('card').values('card','user'))

    #Añadiéndoles un valor número si es like o saved
    ratingLike['rating'] = 1
    ratingSave['rating'] = 2
    #Filtrando los usuarios que una card han hecho like o saved
    userSubsetRating = pd.merge_ordered(ratingLike,ratingSave, how='outer', left_on=['card','user'], right_on=['card','user'])
    userSubsetRating = userSubsetRating.drop_duplicates()
    userSubsetRating['rating_x'] = userSubsetRating['rating_x'].fillna(0)
    userSubsetRating['rating_y'] = userSubsetRating['rating_y'].fillna(0)
    userSubsetRating["rating"] = userSubsetRating['rating_x'].astype(int) + userSubsetRating["rating_y"]
    userSubsetRating = userSubsetRating.drop(columns=['rating_x'])
    userSubsetRating = userSubsetRating.drop(columns=['rating_y'])
    userSubsetRating.to_csv('userSubsetRating.csv')

    #print(userSubsetLike)
    #print("---------------")
    #print(userSubsetSave)

    #Combinando las columnas de saved y like en una sumatoria
    userSubsetLike = ratingLike[ratingLike['card'].isin(inputCards['card'].tolist())]
    userSubsetSave = ratingSave[ratingSave['card'].isin(inputCards['card'].tolist())]
    userSubset = pd.merge(userSubsetLike,userSubsetSave, how='outer', left_on=['card','user'], right_on=['card','user'])
    userSubset.drop_duplicates()
    userSubset = userSubset.drop_duplicates()
    userSubset['rating_x'] = userSubset['rating_x'].fillna(0)
    userSubset['rating_y'] = userSubset['rating_y'].fillna(0)
    userSubset["rating"] = userSubset['rating_x'].astype(int) + userSubset["rating_y"]
    userSubset = userSubset.drop(columns=['rating_x'])
    userSubset = userSubset.drop(columns=['rating_y'])
    userSubset.to_csv('userSubset.csv')

    #Groupby crea varios dataframes donde todos tienen el mismo valor para la columna especificada como parámetro
    userSubsetGroup = userSubset.groupby(['user'])
    print(userSubsetGroup)
    print("//////////////////////////////////")
    #Ordenamiento de forma tal de que los usuarios con más películas en común tengan prioridad
    userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)
    
    inputCards.to_csv('inputCards.csv')

    #Cálculo de la correlación de pearson
    pearsonDF=pearson_correlation(userSubsetGroup,inputCards)

    #Ordenamos los usuarios respecto a su mayor índice de similitud
    topUsers = pearsonDF.sort_values(
        by='similarityIndex', ascending=False)[0:50]
    #print(topUsers)
    topUsersRating = topUsers.merge(userSubsetRating, left_on='user', right_on='user', how='inner')
    # Se multiplica la similitud de los puntajes de los usuarios
    topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * \
        topUsersRating['rating']

    # Se aplica una suma a los topUsers luego de agruparlos por userId
    tempTopUsersRating = topUsersRating.groupby(
        'card').sum()[['similarityIndex', 'weightedRating']]
    tempTopUsersRating.columns = ['sum_similarityIndex', 'sum_weightedRating']

    # Se crea un dataframe vacío
    recommendation_df = pd.DataFrame()
    # Ahora se toma el promedio ponderado
    recommendation_df['card'] = tempTopUsersRating.index
    recommendation_df['score'] = tempTopUsersRating['sum_weightedRating'] / \
        tempTopUsersRating['sum_similarityIndex']
    recommendation_df = recommendation_df.sort_values(
        by='score', ascending=False)
    recommendation_df.to_csv("topUsersRating.csv")

    recommendation_df = recommendation_df.head(10)
    recommendation_df.to_csv("Suggesiton.csv")
    cardList = Card.objects.filter(
        id__in=recommendation_df.head(10).index).values()

    return list(cardList)
    # return tempTopUsersRating.head(10)
    # return recommendation_df['score'].head(10)


def pearson_correlation(userSubsetGroup, inputCards):
    # Guardar la Correlación Pearson en un diccionario, donde la clave es el Id del usuario y el valor es el coeficiente
    pearsonCorrelationDict = {}
    for name, group in userSubsetGroup:
        # Comencemos ordenando el usuario actual y el ingresado de forma tal que los valores no se mezclen luego
        group = group.sort_values(by='card')
        inputCards = inputCards.sort_values(by='card')
        # Obtener el N para la fórmula
        nRatings = len(group)
        # Obtener los puntajes de revisión para las cards en común
        temp_df = inputCards[inputCards['card'].isin(group['card'].tolist())]
        # Guardarlas en una variable temporal con formato de lista para facilitar cálculos futuros
        tempRatingList = temp_df['rating'].tolist()
        # Pongamos también las revisiones de grupos de usuarios en una lista
        tempGroupList = group['rating'].tolist()
        # Calculemos la Correlación Pearson entre dos usuarios, x e y
        Sxx = sum([i**2 for i in tempRatingList]) - \
            pow(sum(tempRatingList), 2)/float(nRatings)
        Syy = sum([i**2 for i in tempGroupList]) - \
            pow(sum(tempGroupList), 2)/float(nRatings)
        Sxy = sum(i*j for i, j in zip(tempRatingList, tempGroupList)) - \
            sum(tempRatingList)*sum(tempGroupList)/float(nRatings)

        # Si el denominador es diferente a cero, entonces dividir, sino, la correlación es 0.
        if Sxx != 0 and Syy != 0:
            #print(Sxx)
            #print(Syy)
            #print(Sxy)
            #print("-")
            pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
            
        else:
            pearsonCorrelationDict[name] = 0
    pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
    pearsonDF.columns = ['similarityIndex']
    pearsonDF['user'] = pearsonDF.index
    pearsonDF.index = range(len(pearsonDF))
    #Ordenamos los usuarios respecto a su mayor índice de similitud
    
    return pearsonDF

def pearson_correlation_i(userOne , userTwo, userRating: pd.DataFrame):
    # Guardar la Correlación Pearson en un diccionario, donde la clave es el Id del usuario y el valor es el coeficiente
    pearsonCorrelation = 0
    #for name, group in userSubsetGroup:
    #print(userRating.where(userRating['user'] == userOne).dropna())
    inputCards = userRating.where(userRating['user'] == userOne).dropna()
    toEvaluate = userRating.where(userRating['user'] == userTwo).dropna()
    toEvaluate = toEvaluate[toEvaluate['card'].isin(inputCards['card'].tolist())]
    if(toEvaluate.empty):
        pearsonCorrelation = 0
        return pearsonCorrelation
    # Obtener el N para la fórmula
    nRatings = len(toEvaluate)
    # Obtener los puntajes de revisión para las cards en común
    temp_df = inputCards[inputCards['card'].isin(toEvaluate['card'].tolist())]
    # Guardarlas en una variable temporal con formato de lista para facilitar cálculos futuros
    tempRatingList = temp_df['rating'].tolist()

    # Pongamos también las revisiones de grupos de usuarios en una lista
    tempGroupList = toEvaluate['rating'].tolist()

    # Calculemos la Correlación Pearson entre dos usuarios, x e y
    Sxx = sum([i**2 for i in tempRatingList]) - \
        pow(sum(tempRatingList), 2)/float(nRatings)
    Syy = sum([i**2 for i in tempGroupList]) - \
        pow(sum(tempGroupList), 2)/float(nRatings)
    Sxy = sum(i*j for i, j in zip(tempRatingList, tempGroupList)) - \
        sum(tempRatingList)*sum(tempGroupList)/float(nRatings)

    # Si el denominador es diferente a cero, entonces dividir, sino, la correlación es 0.
    if Sxx != 0 and Syy != 0:
        #print(Sxx)
        #print(Syy)
        #print(Sxy)
        #print("-")
        pearsonCorrelation= Sxy/sqrt(Sxx*Syy)
        
    else:
        pearsonCorrelation = 0
    return pearsonCorrelation


#Cálculo de vecinos cercanos
def calculate_neighbors(similarities_matrix, k_neighbors):
    
    neighbors = [None for _ in range(len(similarities_matrix))]
    print(neighbors)
    for index, similarities in similarities_matrix.iterrows():
        #print(index)
        #print(similarities)
        #print("---")
        i_neighbors = [i[0] for i in sorted(enumerate(similarities), 
                                            key=lambda x:float('-inf') if x[1] is None else x[1], 
                                            reverse=True)]
        #print(index)
        #print(i_neighbors[0:k_neighbors])
        neighbors[index-1] = i_neighbors[0:k_neighbors]

    return neighbors

def knn():
    ratingLike = pd.DataFrame(Like.objects.all().order_by('card').values('card','user'))
    ratingSave = pd.DataFrame(Save.objects.all().order_by('card').values('card','user'))
    userList = list(User.objects.values('id'))

    #Añadiéndoles un valor número si es like o saved
    ratingLike['rating'] = 1
    ratingSave['rating'] = 2
    #Filtrando los usuarios que una card han hecho like o saved
    userRating = pd.merge_ordered(ratingLike,ratingSave, how='outer', left_on=['card','user'], right_on=['card','user'])
    userRating = userRating.drop_duplicates()
    userRating
    userRating['rating_x'] = userRating['rating_x'].fillna(0)
    userRating['rating_y'] = userRating['rating_y'].fillna(0)
    userRating["rating"] = userRating['rating_x'].astype(int) + userRating["rating_y"]
    userRating = userRating.drop(columns=['rating_x'])
    userRating = userRating.drop(columns=['rating_y'])
    userRating.to_csv('userSubsetRating.csv')
    
    #   print(userRating.values().tolist())
    
    userRatingMatrix = userRating.pivot(index='user',columns='card',values='rating').fillna(0)
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=1)
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=0)

    userRatingMatrix.to_csv("userRatingMatrix.csv")
    df = pd.DataFrame()
    #userRatingMatrix.columns = ["C".format(+np.array(userRating['card'].sort_values().drop_duplicates()))]
    #print(matrix.unstack(-1))
    
    userRatingUser = userRating['user'].sort_values().drop_duplicates().reset_index(drop=True)
    similarity = 0
    userMatrix = pd.DataFrame(columns=['userOne','userTwo','similarity'])

    #p1 = pearson_correlation_i(58,1,userRating)
    #p2 = pearson_correlation_i(1,58,userRating)
    #print(p1)
    #print(p2)
    #return 1

    #class Found(Exception): pass
    #try:
    #    for userOne in userRatingUser:
    #        for userTwo in userRatingUser:
    #            if(userOne != userTwo):
    #                similarity = pearson_correlation_i(userOne, userTwo, userRating)
    #            else:
    #                similarity = float('-inf')
    #            
    #            if(userOne==102):
    #                raise Found
    #            #print(str(userOne) + "-" + str(userTwo))
    #            temp_pd = pd.DataFrame([[userOne,userTwo,similarity]],columns=['userOne','userTwo','similarity'])
    #            userMatrix = pd.concat([userMatrix,temp_pd])
    #            #print(userMatrix)
    #except Found:
    #    userMatrix.to_csv("userMatrix.csv")
    #userMatrix = userMatrix.pivot(index='userOne',columns='userTwo',values='similarity')
    #userMatrix.to_csv("userMatrix.csv")
    
    userMatrix = pd.read_csv('userMatrix.csv')
    #print(userMatrix.head(10))
    userLabels = userRating['card'].drop_duplicates().sort_values()
    neighbors = calculate_neighbors(userMatrix,20)
    print(neighbors)

    dataK=np.array([np.array(xi) for xi in neighbors])
    print(dataK)
    userLabel=[str(i) for i in userRatingUser]
    cardLabel=[str(i) for i in userLabels][0:20]
    print(userLabel)
    print(cardLabel)
    userNeighbors = pd.DataFrame(data=dataK,
                        index=userLabel,
                        columns=cardLabel)

    print(userNeighbors)
    #print(userRatingMatrix)
    
    #print(userMatrix.values.tolist())
    aux_sim = [[userMatrix.values.tolist()[index_u][neighbord] for index_j, neighbord in enumerate(user)] 
           for index_u, user in enumerate(neighbors)]

    matrixToPrint = pd.DataFrame(data=np.array([np.array(xi) for xi in aux_sim]),
                index=userLabel,
                columns=cardLabel)
    
    print(matrixToPrint)
