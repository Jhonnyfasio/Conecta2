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
        #knn()
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
        return JsonResponse({'message':'Success, pearson matrix made'})

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
    #userSubsetRating.to_csv('userSubsetRating.csv')

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
    #Ordenamiento de forma tal de que los usuarios con más cards en común tengan prioridad
    userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)
    
    inputCards.to_csv('inputCards.csv')

    #Cálculo de la correlación de pearson
    pearsonDF=pearson_correlation(userSubsetGroup,inputCards)

    #Ordenamos los usuarios respecto a su mayor índice de similitud
    topUsers = pearsonDF.sort_values(
        by=['similarityIndex','user'], ascending=[False,True])[0:7]
    #print(topUsers)
    topUsersRating = topUsers.merge(userSubsetRating, left_on='user', right_on='user', how='inner')
    #print(topUsersRating)
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
    ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(recommendation_df.head(10).index)])
    cardList = Card.objects.filter(
        id__in=recommendation_df.head(10).index).annotate(isLike=Count(
            'like_card', filter=Q(like_card__status=True, like_card__user_id__in=recommendation_df.head(10).index))).annotate(isSave=Count(
                'save_card', filter=Q(save_card__status=True, save_card__user_id__in=recommendation_df.head(10).index))).annotate(countLike=Count(
                    'like_card', filter=Q(like_card__status=True))).order_by(ordering).values()
    
    return list(cardList)



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
    userRating
    userRating['rating_x'] = userRating['rating_x'].fillna(0)
    userRating['rating_y'] = userRating['rating_y'].fillna(0)
    userRating["rating"] = userRating['rating_x'].astype(int) + userRating["rating_y"]
    userRating = userRating.drop(columns=['rating_x'])
    userRating = userRating.drop(columns=['rating_y'])
    #userRating.to_csv('userSubsetRating.csv')
    
    #   print(userRating.values().tolist())
    userRatingMatrix = userRating.pivot(index='user',columns='card',values='rating').fillna('None')
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=1)
    userRatingMatrix = userRatingMatrix.rename_axis(None,axis=0)
    userRatingMatrix = userRatingMatrix.reset_index(drop=True)
    userRatingMatrix = userRatingMatrix.T.reset_index(drop=True).T

    #userRatingMatrix.to_csv("userRatingMatrix.csv")
    df = pd.DataFrame()
    #userRatingMatrix.columns = ["C".format(+np.array(userRating['card'].sort_values().drop_duplicates()))]
    #print(matrix.unstack(-1))
    
    userRatingUser = userRating['user'].sort_values().drop_duplicates().reset_index(drop=True)
 
    userSimilarityDF = pd.read_csv('userMatrix.csv',index_col=0)
    userSimilarityDF = userSimilarityDF.rename_axis(None,axis=0)
    temp_cardList = pd.read_csv('userSubsetRating.csv')
    #print(userMatrix.head(10))
    userLabel = userSimilarityDF.index.tolist()

    cardLabel = temp_cardList['card'].drop_duplicates().tolist()
   
    k = 7
    neighbors = calculate_neighbors(userSimilarityDF,k)
    #print(len(neighbors))
    #print(neighbors)
    userRating.to_csv('userRating.csv')
    #print(dataK)
    #userNeighbors = pd.DataFrame.from_dict(neighbors,orient='index')

    #print(userNeighbors)
    #print(userRatingMatrix)
    
    #print(userMatrix.values.tolist())
    #print(userSimilarityDF.values.tolist())
    #aux_sim = [[userSimilarityDF.values.tolist()[index_u][neighbord] for index_j, neighbord in enumerate(user)] 
    #       for index_u, user in enumerate(neighbors)]
    
    #for index_u, user in enumerate(neighbors):
    #    #print(index_u)
    #    #print(user)
    #    for index_j, neighbord in enumerate(user):
    #        None
    #        userSimilarityDF.values.tolist()[index_u][neighbord]


    #print(aux_sim)
    #matrixToPrint = pd.DataFrame(data=np.array([np.array(xi) for xi in neighbors]),
    #            index=userLabel,
    #            columns=[i for i in range(k)])
    #print(matrixToPrint)

    #matrixToPrint = pd.DataFrame(data=np.array([np.array(xi) for xi in aux_sim]),
    #            index=["U{}".format(str(i)) for i in range(len(matrixToPrint))],
    #            columns=["K{}".format(str(i)) for i in range(k)])
    #print(matrixToPrint)
    #print(userRatingMatrix.values.tolist())
    
    predictions = [[None for _ in range(len(cardLabel))] for _ in range(len(userLabel))]
    #userRatingList = userRatingMatrix.values.tolist()
    userRatingCSV = pd.read_csv("userSubsetRating.csv",index_col=0)
    userRatingMatrix = userRatingCSV.pivot(index='user',columns='card',values='rating').fillna('None')
    #userRatingMatrix = userRatingMatrix.rename_axis(None,axis=0)
    #userRatingMatrix = userRatingMatrix.rename_axis(None,axis=1)
    #print(userRatingList.values.tolist())
    #userRatingList = userRatingList.values.tolist()
    #print(userRatingMatrix)
    pd.DataFrame(neighbors).to_csv("neighbors.csv")

    # Crear una matriz para el cálculo de predicciones
    predictions = [[None for _ in range(len(cardLabel))] for _ in range(len(userLabel))]
    
    userSimilarityList = userSimilarityDF.values.tolist()
    userRatingMatrix_iterr = userRatingMatrix.iterrows()
    print(userRatingMatrix)
    userRatingMatrix.to_csv("userRatingMatrix.csv")
    #print(userSimilarityList)
    #print(userRatingList[1][3])
    # Recorrer la matriz de votos
    #print(userRatingMatrix.iterrows())e
    #print(userRatingMatrix.values)
    #print(userLabel)
    #print(userRatingList[16][3])
    #print(userSimilarityList)
    #print(neighbors)
    #return
    userRatingList = userRatingMatrix.values.tolist()
    #print(userRatingList[99])
    #print(type(userRatingList))
    ###print("///")
    #print(neighbors)
    #print(type(userSimilarityList))
    i = 0
    #print(userSimilarityDF)
    print(neighbors)
    for user, m in enumerate(userLabel):
    #for user in userLabel: 
        #print(user)
        j = 0
        for card, n in enumerate(cardLabel):
        #for card in cardLabel:
            numerador = 0 
            denominador = 0
            #print("neighbors of " +str(user) +" - ")
            #print(neighbors[i])
            for neighbor in neighbors[user]:
                #condition = (userRatingList['user'] == user & (userRatingList['card'] == card))
                #print(userRatingList[condition]['rating'])
                #if userRatingList[condition]['rating'] != "None":
                #print(userRatingMatrix.at[1,1])
                #print(type(user))
                #print(type(card))
                #(neighbor)
                #print("neigh")
                if userRatingMatrix.iloc[neighbor, card] != "None":
                #print(type(neighbor))
                #print(type(user))
                #print(type(card))
                #print(userSimilarityList[user][neighbor])
                #print(userRatingList[neighbor][card])
                #if(neighbor == 100):
                    #print(str(user) + " - " + str(neighbor) + " - " + str(card))
                #if userRatingList[neighbor-1][card] != "None":
                #    None
                #print(neighbor)
                #if userRatingList[neighbor][j] != "None":
                #print(userRatingList[(userRatingList['user'] == neighbor) & (userRatingList['card'] == j)]['rating'].tolist())
                #if userRatingList[(userRatingList['user'] == neighbor) & (userRatingList['card']== j)]['rating'].tolist() != "None":
                    #print(userRatingList[neighbor][j])
                    #print(str(user) + " - " + str(j))
                    #print("//")
                    #print(userMatrix.values.tolist()[user][neighbor])
                    #print(userRatingList[neighbor][j])
                    #print(userSimilarityDF.at[user, neighbor])
                    #print(userSimilarityList[user][neighbor])
                    #print(userSimilarityList[user][neighbor])
                    
                    #print("usr: " + str(user) + " card: " + str(card) + " neigh: " + str(neighbor))
                    #print(userSimilarityDF.iloc[user, neighbor])
                    #print( userRatingMatrix.iloc[neighbor, card])
                    numerador += (userSimilarityDF.iloc[user, neighbor] * userRatingMatrix.iloc[neighbor, card])
                    #numerador += (userSimilarityList[user][neighbor-1] * userRatingList[neighbor-1][card])
                    denominador += userSimilarityDF.iloc[user, neighbor]
                    
            predictions[i][j] = (None if denominador == 0 
                                else numerador/denominador)
            j+=1
        i+=1

    #print(predictions)
    pd.DataFrame(data=predictions,index=userLabel,columns=cardLabel).to_csv("predictions.csv")
    #print(userRatingList)
    recommendations = make_recommendations(30,userRatingList,predictions)
    #print(recommendations)
    pd.DataFrame(recommendations).to_csv("recommendations.csv")
    #print(len(userRatingList))
    #print(len(userRatingList))
    #print(matrixToPrint)
    #print(stack.head(30))
    #print(userRatingMatrix)

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
    
    userRatingUser = userRating['user'].sort_values().drop_duplicates().reset_index(drop=True)
    similarity = 0
    userMatrix = pd.DataFrame(columns=['userOne','userTwo','similarity'])


    for userOne in userRatingUser:
        for userTwo in userRatingUser:
            if(userOne != userTwo):
                similarity = pearson_correlation_i(userOne, userTwo, userRating)
            else:
                similarity = float('-inf')
            
            #print(str(userOne) + "-" + str(userTwo))
            temp_pd = pd.DataFrame([[userOne,userTwo,similarity]],columns=['userOne','userTwo','similarity'])
            userMatrix = pd.concat([userMatrix,temp_pd])

    userMatrix = userMatrix.pivot(index='userOne',columns='userTwo',values='similarity')
    userMatrix.to_csv("userMatrix.csv")


def make_recommendations(num_recomendations, ratings_matrix, predictions_matrix):
    
    # Crear una matriz para las recomendaciones
    recommendations = [[(None, None) for _ in range(num_recomendations)] for _ in range(len(ratings_matrix))]

    # Recorrer la matriz de votos
    for i, u in enumerate(ratings_matrix):
        for j, v in enumerate(ratings_matrix[0]):
            if ratings_matrix[i][j] == "None":
                recommendations[i].append((j, predictions_matrix[i][j]))
        
        # Ordenar los items a recomendar al usuario
        recommendations[i] = sorted(recommendations[i], 
                                    key=lambda x:float('-inf') if x[1] is None else x[1], 
                                    reverse=True)[0:num_recomendations]

    return [[x[0] for x in reco_user] for reco_user in recommendations]
