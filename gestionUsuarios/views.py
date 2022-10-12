from http.client import HTTPResponse
from operator import pos
from unicodedata import category
from xml.etree.ElementTree import tostring
from django.http.response import JsonResponse
from django.db.models import Count, Q, Case, When
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Card as CardGU, User as UserGU, Like as LikeGU
from api.models import CardPost as Card, Category, User, Like, Save
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

class Pearson(View):
    def get(self, request):      
        pearson_correlation_all()
        return JsonResponse({'message':'Success, pearson matrix done'})

class Recommendation(View):
    def get(self, request):
        knn()
        return JsonResponse({'message':'Success, recommendations matrix done'})

class PearsonRecommendation(View):
    def get(self, request, idUser):
        recommendation = get_recommendation(idUser)
        print(recommendation)
        if len(recommendation) > 0:
            data = {'message': 'Success', 'cards': recommendation}
        else:
            data = {'message': 'No cards to suggest'}
        return JsonResponse(data)



def Suggestion(idUser):
    print('unziping ...')

    #Guardar la información de las tarjetas y usuarios en un QuerySet
    #movies_df = pd.read_csv('movies.csv')
    cardList = list(Card.objects.exclude(user=idUser).values('id', 'user'))
    userList = list(User.objects.values('id'))
    likeList = Like.objects.exclude(user=idUser).values('id','user','card','status')
    saveList = Save.objects.exclude(user=idUser).values('id','user','card','status')

    #Comprobar datos para iterar
    if len(cardList) <= 0 or len(userList) <= 0  or len(list(likeList)) <= 0 or len(list(saveList)) <= 0:
        return JsonResponse({"message:": "Failure, no data found"})
    #Extraer las cards con like y saved del usuario a sugerir y guardado en un dataframe
    inputCardsLike = pd.DataFrame(Like.objects.filter(user=idUser).order_by('card').values('card'))
    inputCardsSave = pd.DataFrame(Save.objects.filter(user=idUser).order_by('card').values('card'))
    if inputCardsLike.empty and inputCardsSave.empty:
        return JsonResponse({"message:": "Failure, no data found"})
    #print(inputCardsLike)
    inputCardsLike.to_csv("inputCardsLike.csv")
    inputCardsSave.to_csv("inputCardsSave.csv")
    #Añadir un valor numérico si es saved o like
    inputCardsLike['rating'] = int(1)
    inputCardsSave['rating'] = int(2)
    #Combinar las columnas de saved y like de entrada del usuario en una sumatoria
    try:
        inputCards = pd.merge_ordered(inputCardsLike,inputCardsSave,how='outer', left_on=['card'], right_on=['card']).sort_values('card')
    except:
        inputCards = inputCardsLike if not inputCardsLike.empty else inputCardsSave
    inputCards = inputCards.drop_duplicates()
    
    if not inputCardsLike.empty and not inputCardsSave.empty:
        inputCards['rating_x'] = inputCards['rating_x'].fillna(0)
        inputCards['rating_y'] = inputCards['rating_y'].fillna(0)
        inputCards['rating'] = inputCards['rating_x'].astype(int) + inputCards['rating_y']
        inputCards = inputCards.drop(columns=['rating_x'])
        inputCards = inputCards.drop(columns=['rating_y'])
    else:
        inputCards['rating'] = inputCards['rating'].fillna(0)
    
    #Guardar en CSV para respaldo.
    inputCards.to_csv('inputCards.csv')

    #///////////////////////////////////////////////////
    #Guardar información de todas las cards con like y las guardadas en un dataframe, excluyendo las del usuario a sugerir
    ratingLike = pd.DataFrame(likeList.values('card','user'))
    ratingSave = pd.DataFrame(saveList.values('card','user'))
    Like.objects.exclude(user=idUser).values('id','user','card','status')

    #Añadir un valor número si es like o saved
    ratingLike['rating'] = 1
    ratingSave['rating'] = 2
    #Filtrar los usuarios que una card han hecho like o saved
    userSubsetRating = pd.merge_ordered(ratingLike,ratingSave, how='outer', left_on=['card','user'], right_on=['card','user'])
    userSubsetRating = userSubsetRating.drop_duplicates()
    userSubsetRating['rating_x'] = userSubsetRating['rating_x'].fillna(0)
    userSubsetRating['rating_y'] = userSubsetRating['rating_y'].fillna(0)
    userSubsetRating["rating"] = userSubsetRating['rating_x'].astype(int) + userSubsetRating["rating_y"]
    userSubsetRating = userSubsetRating.drop(columns=['rating_x'])
    userSubsetRating = userSubsetRating.drop(columns=['rating_y'])

    #Combinar las columnas de saved y like en una sumatoria
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
    #print(userSubsetGroup)
    #print("//////////////////////////////////")
    #Ordenar de forma tal de que los usuarios con más cards en común tengan prioridad
    userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)
    
    inputCards.to_csv('inputCards.csv')

    #Calcular de la correlación de pearson
    pearsonDF=pearson_correlation(userSubsetGroup,inputCards)

    #Ordenamos los usuarios respecto a su mayor índice de similitud
    topUsers = pearsonDF.sort_values(
        by=['similarityIndex','user'], ascending=[False,True])[0:10]
    print(topUsers)
    topUsersRating = topUsers.merge(userSubsetRating, left_on='user', right_on='user', how='inner')
    #print(topUsersRating)
    topUsersRating.to_csv("top.csv")
    topUsersRating = topUsersRating[~topUsersRating['card'].isin(inputCards['card'].tolist())]
    # Se multiplica la similitud de los puntajes de los usuarios
    topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * \
        topUsersRating['rating']
    #print("ASASAS")
    #print(topUsersRating['rating'])
    #print(topUsersRating['similarityIndex'])
    #print(topUsersRating.head(100))

    # Se aplica una suma a los topUsers luego de agruparlos por userId
    tempTopUsersRating = topUsersRating.groupby(
        'card').sum()[['similarityIndex', 'weightedRating']]
    tempTopUsersRating.columns = ['sum_similarityIndex', 'sum_weightedRating']
    print(tempTopUsersRating)
    tempTopUsersRating.to_csv("tempTopUserRating.csv")
    # Se crea un dataframe vacío
    recommendation_df = pd.DataFrame()
    # Ahora se toma el promedio ponderado
    #print(tempTopUsersRating.index)
    recommendation_df.index = tempTopUsersRating.index
    recommendation_df['score'] = tempTopUsersRating['sum_weightedRating'] / tempTopUsersRating['sum_similarityIndex']
    recommendation_df = recommendation_df.sort_values(
        by=['score','card'], ascending=[False,True])
    recommendation_df.to_csv("topUsersRating.csv")

    #recommendation_df = recommendation_df.head(10)
    recommendation_df.to_csv("Suggesiton.csv")
    print(recommendation_df.head(10).index)
    user = User.objects.get(id=idUser)
    ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(recommendation_df.head(10).index)])
    cardList = Card.objects.filter(
        id__in=recommendation_df.head(10).index).annotate(isLike=Count(
            'like_card', filter=Q(like_card__status=True, like_card__user_id=user))).annotate(isSave=Count(
                'save_card', filter=Q(save_card__status=True, save_card__user_id=user))).annotate(countLike=Count(
                    'like_card', filter=Q(like_card__status=True))).order_by(ordering).values()
    
    return list(cardList)



def pearson_correlation(userSubsetGroup, inputCards):
    # Guardar la Correlación Pearson en un diccionario, donde la clave es el Id del usuario y el valor es el coeficiente
    pearsonCorrelationDict = {}
    for name, group in userSubsetGroup:
        # Comencemos ordenando el usuario actual y el ingresado de forma tal que los valores no se mezclen luego
        group = group.sort_values(by='card')
        inputCards = inputCards.sort_values(by='card')
        #print(group)
        #print(inputCards)
        #print(".")
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
        #rint(Sxx)
        #print(Syy)
        #print(Sxy)
        #print("-")
        if Sxx != 0 and Syy != 0:
            
            pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
            
        else:
            pearsonCorrelationDict[name] = 0
        
        #print(str(name) + " - " + str(group) + " - " + str(pearsonCorrelationDict[name]))
    pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
    pearsonDF.columns = ['similarityIndex']
    pearsonDF['user'] = pearsonDF.index
    pearsonDF.index = range(len(pearsonDF))
    #Ordenamos los usuarios respecto a su mayor índice de similitud
    
    return pearsonDF

def pearson_correlation_i(userOne , userTwo, userRating: pd.DataFrame):
    # Guardar la Correlación Pearson en un diccionario, donde la clave es el Id del usuario y el valor es el coeficiente
    pearsonCorrelation = 0
    #https://www.projectpro.io/recipes/search-value-within-pandas-dataframe-column
    #inputCards = userRating.where(userRating['user'] == userOne).dropna().sort_values(by='card')
    #toEvaluate = userRating.where(userRating['user'] == userTwo).dropna().sort_values(by='card')
    inputCards = userRating[inputCards]
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
        pearsonCorrelation= Sxy/sqrt(Sxx*Syy)
    else:
        pearsonCorrelation = 0

    return pearsonCorrelation

#Cálculo de vecinos cercanos
def calculate_neighbors(similarities_matrix, k_neighbors):
    neighbors = [None for _ in range(len(similarities_matrix))]
    #neighbors = dict()
    similarities_matrix_iterr = similarities_matrix.iterrows()
    i=0
    print(similarities_matrix_iterr)
    for index, similarities in similarities_matrix_iterr:
        #print(index)
        #print(similarities)
        i_neighbors = [int(i[0]) for i in sorted(enumerate(similarities), 
                                            key=lambda x:float('-inf') if x[1] is None else x[1], 
                                            reverse=True)]
        #neighbors[index] = i_neighbors[0:k_neighbors]
        neighbors[i] = i_neighbors[0:k_neighbors]
        #print(i_neighbors)
        i+=1
        #print(type(i_neighbors[0:k_neighbors]))

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
    userRating['rating_x'] = userRating['rating_x'].fillna(0)
    userRating['rating_y'] = userRating['rating_y'].fillna(0)
    userRating["rating"] = userRating['rating_x'].astype(int) + userRating["rating_y"]
    userRating = userRating.drop(columns=['rating_x'])
    userRating = userRating.drop(columns=['rating_y'])

    userRatingMatrix = userRating.pivot(index='user',columns='card',values='rating').fillna('None')
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=1)
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=0)
    userRatingMatrix = userRatingMatrix.reset_index(drop=True)
    userRatingMatrix = userRatingMatrix.T.reset_index(drop=True).T
 
    userSimilarityDF = pd.read_csv('userMatrix.csv',index_col=0)
    userSimilarityDF = userSimilarityDF.rename_axis(None,axis=0)
    temp_cardList = pd.read_csv('userSubsetRating.csv')
    #print(userMatrix.head(10))
    userLabel = userSimilarityDF.index.tolist()
    cardLabel = temp_cardList['card'].drop_duplicates().tolist()
   
    k = 10
    neighbors = calculate_neighbors(userSimilarityDF,k)
    userRating.to_csv('userRating.csv')
    
    predictions = [[None for _ in range(len(cardLabel))] for _ in range(len(userLabel))]
    #userRatingList = userRatingMatrix.values.tolist()
    userRatingCSV = pd.read_csv("userSubsetRating.csv",index_col=0)
    userRatingMatrix = userRatingCSV.pivot(index='user',columns='card',values='rating').fillna('None')

    pd.DataFrame(neighbors).to_csv("neighbors.csv")

    # Crear una matriz para el cálculo de predicciones
    predictions = [[None for _ in range(len(cardLabel))] for _ in range(len(userLabel))]
    
    userSimilarityList = userSimilarityDF.values.tolist()
    #print(userRatingMatrix)
    userRatingMatrix.to_csv("userRatingMatrix.csv")
    userRatingList = userRatingMatrix.values.tolist()

    for user, m in enumerate(userLabel):
        for card, n in enumerate(cardLabel):
            numerador = 0 
            denominador = 0
            for neighbor in neighbors[user]:
                if userRatingList[neighbor][card] != "None":
                    numerador += (userSimilarityList[user][neighbor] * userRatingList[neighbor][card])
                    denominador += userSimilarityList[user][neighbor]
                    
            predictions[user][card] = (None if denominador == 0 
                                else numerador/denominador)

    #print(predictions)
    pd.DataFrame(data=predictions,index=userLabel,columns=cardLabel).to_csv("predictions.csv")
    #pd.DataFrame(predictions).to_csv("predictions.csv")
    #print(userRatingList)
    recommendations = make_recommendations(100,userRatingList,predictions, userLabel, cardLabel)
    #print(recommendations)
    pd.DataFrame(recommendations, index=userLabel).to_csv("recommendations.csv")

def pearson_correlation_all():
    ratingLike = pd.DataFrame(Like.objects.all().order_by('card').values('card','user'))
    ratingSave = pd.DataFrame(Save.objects.all().order_by('card').values('card','user'))

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
    userRatingMatrix = userRating.pivot(index='user',columns='card',values='rating').fillna('None')
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=1)
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=0)
    userRatingList = userRatingMatrix.values.tolist()

    print(userRatingMatrix)
    
    userRatingUser = userRating['user'].sort_values().drop_duplicates().reset_index(drop=True)
    similarity = 0
    userMatrix = pd.DataFrame(columns=['userOne','userTwo','similarity'])

    for userOne, x in enumerate(userRatingUser):
        if(userOne <= 10):
            for userTwo, y in enumerate(userRatingUser):
                if(userOne != userTwo):
                    similarity = pearson_correlation_i(userOne, userTwo, userRatingList)
                    None
                else:
                    similarity = float('-inf')
                    None
            
            #temp_pd = pd.DataFrame([[userOne,userTwo,similarity]],columns=['userOne','userTwo','similarity'])
            #userMatrix = pd.concat([userMatrix,temp_pd])
            print(str(userOne) + "-" + str(userTwo))

    userMatrix = userMatrix.pivot(index='userOne',columns='userTwo',values='similarity')

def make_recommendations(num_recomendations, ratings_matrix, predictions_matrix, userLabel, cardLabel):
    # Crear una matriz para las recomendaciones
    recommendations = [[(None, None) for _ in range(num_recomendations)] for _ in range(len(ratings_matrix))]
    # Recorrer la matriz de votos
    #print(predictions_matrix)
    for i, u in enumerate(ratings_matrix):
        #print(str(i) + " - " + str(u)) 
        for j, v in enumerate(ratings_matrix[0]):
            #print(v)
            #print(str(j) + " - " + str(predictions_matrix[i][j]))
            if ratings_matrix[i][j] == "None":
                #print((int(userLabel[j])))
                if(predictions_matrix[i][j] != None):
                    recommendations[i].append((cardLabel[j], predictions_matrix[i][j]))  
        # Ordenar los items a recomendar al usuario
        recommendations[i] = sorted(recommendations[i], 
                                    key=lambda x:float('-inf') if x[1] is None else x[1], 
                                    reverse=True)[0:num_recomendations]

    return [[x[0] for x in reco_user] for reco_user in recommendations]

def get_recommendation(idUser):
    recommendationsMatrix = pd.read_csv("recommendations.csv",index_col=0)
    recommendation = recommendationsMatrix.loc[idUser]
    user = User.objects.get(id=idUser)
    ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(recommendation.values.tolist())])
    cards = list(Card.objects.filter(id__in=recommendation.values.tolist()).annotate(isLike=Count(
            'like_card', filter=Q(like_card__status=True, like_card__user_id=user))).annotate(isSave=Count(
                'save_card', filter=Q(save_card__status=True, save_card__user_id=user))).annotate(countLike=Count(
                    'like_card', filter=Q(like_card__status=True))).order_by(ordering).values())

    return cards
    
