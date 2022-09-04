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
        # return JsonResponse({'message': list(Card.objects.filter(user=id_user).values())})
        dataFrame = Suggestion(id_user)
        print(dataFrame)
        if len(dataFrame) > 0:

            #data = {'message': 'Success', 'cards': json.dumps(dataFrame.values.tolist())}
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
    #!wget -O moviedataset.zip https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/moviedataset.zip
    print('unziping ...')
    #!unzip -o -j moviedataset.zip

    # Guardando la información de la película dentro de un dataframe de panda
    #movies_df = pd.read_csv('movies.csv')
    cardList = list(Card.objects.values('id', 'user'))
    userList = list(User.objects.values('id'))
    likeList = list(Like.objects.values('id', 'user', 'card', 'status'))
    saveList = list(Save.objects.values('id', 'user', 'card', 'status'))
    if len(cardList) <= 0 or len(userList) <= 0 or len(likeList) <= 0 or len(saveList) <= 0:
        data = {"message:": "Failure, no data found"}
        return JsonResponse(data)

    # Guardando información del usuario dentro de un dataframe de panda
    #ratings_df = pd.read_csv('ratings.csv')

    # userInput = [
    #            {'title':'Breakfast Club, The', 'rating':5},
    #            {'title':'Toy Story', 'rating':3.5},
    #            {'title':'Jumanji', 'rating':2},
    #            {'title':"Pulp Fiction", 'rating':5},
    #            {'title':'Akira', 'rating':4.5}
    #        ]

    userLike = Like.objects.filter(
        user=idUser, status=True).order_by('card').values('card')

    userSave = Save.objects.filter(
        user=idUser, status=True).order_by('card').values('card')

    # cards = list(Card.objects.annotate(isLike=Count(
    #        'like_card', filter=Q(like_card__status=True, like_card__user_id=idUser))).annotate(isSave=Count(
    #            'save_card', filter=Q(save_card__status=True, save_card__user_id=idUser))).annotate(countLike=Count(
    #                'like_card', filter=Q(like_card__status=True))).values('id', 'isLike', 'isSave'))
    # print(cards)

    # print(userLike)
    #userSave = list(userSave)
    # print(userSave)
    userInput = list()
    userInput = {}

    for card in userLike:

        # print(card)
        # userInput[card.get('card')]['rating']({card.get('card'):{'rating':1}})
        value = card.get('card')
        userInput[value] = {}
        userInput[value]['rating'] = 1

    # print(userInput)
    # for card in userInput:
    #    print(userSave.get(card=card['id']))
    #    #print(dir(userSave))
    #    #userSave
    #    #print(card['id'])
    #    #userSavedCard =
    #
    #    if userSave.get(card=card['id']):
    #        print("con"+str(card['id'])+" se encontró "+str(userSave.get(card=card['id'])))
    #        card['rating'] += 3
    #    else:
    #        #userInput += [{'id':,'rating':2}]
    #        print("nada")

    # print(userInput)
    for card in userSave:
        userInput.items()
        #cardToFind = [{card.get('card'):{'rating':1}}]
        #print("buscando: "+str(cardToFind))
        if userInput.get(card.get('card')):
            # if userInput[card.get('card')]:
            cardToFind = card.get('card')
            #print({'card':card.get('card')} in userInput)
            # print(userInput.index(cardToFind))
            # print(userInput[1])
            userInput[cardToFind]['rating'] = 3
            # print(userInput[cardToFind])
        else:
            print("nada")
            value = card.get('card')
            userInput[value] = {}
            userInput[value]['rating'] = 2
        # if userInput.index({'id':card.get('card'),'rating':1}):
            # print(userInput.index({'id':card.get('card'),'rating':1}))

    # print(userInput)
    print(userInput)
    inputCards = pd.DataFrame(userInput)

    # Filtrar las películas por título
    #inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]

    # Luego juntarlas para obtener el movieId. Implícitamente, lo está uniendo por título.
    #inputMovies = pd.merge(inputId, inputMovies)

    # Eliminando información que no utilizaremos del dataframe de entrada
    #inputMovies = inputMovies.drop('year', 1)

    # Dataframe de entrada final

    # Si una película que se agregó no se encuentra, entonces podría no estar en el dataframe

    # original o podría estar escrito de otra forma, por favor revisar mayúscula o minúscula.
    # inputMovies

    inputCards2 = [
        {'card': 1, 'rating': 1},
        {'card': 2, 'rating': 2},
        {'card': 3, 'rating': 2},
        {'card': 10, 'rating': 3},
        {'card': 11, 'rating': 3}
    ]
    inputCards = pd.DataFrame(inputCards2)
    print(inputCards)
    ratingLike = pd.DataFrame(Like.objects.exclude(
        user=idUser).order_by('card').values('card', 'user'))
    ratingSave = pd.DataFrame(Save.objects.exclude(
        user=idUser).order_by('card').values('card', 'user'))
    ratingLike['rating'] = 1
    ratingSave['rating'] = 2

    inputCardsLike = pd.DataFrame(Like.objects.filter(
        user=idUser).order_by('card').values('card'))
    inputCardsSave = pd.DataFrame(Save.objects.filter(
        user=idUser).order_by('card').values('card'))
    inputCardsLike['rating'] = int(1)
    inputCardsSave['rating'] = int(2)
    inputCards = pd.merge(inputCardsLike, inputCardsSave,
                          how='outer', left_on=['card'], right_on=['card'])
    inputCards = inputCards.drop_duplicates()
    inputCards['rating_x'] = inputCards['rating_x'].fillna(0)
    inputCards['rating_y'] = inputCards['rating_y'].fillna(0)
    inputCards['rating'] = inputCards['rating_x'].astype(
        int) + inputCards['rating_y']
    inputCards = inputCards.drop('rating_x', 1)
    inputCards = inputCards.drop('rating_y', 1)
    print(inputCards)
    inputCards.to_csv('inputCards.csv')
    inputCards = inputCards.head(20)

    #inputCards = pd.DataFrame(inputCards2)

    print(ratingLike)
    # print(ratingSave)
    print("//////////////////////////////")
    # print(inputCards)

    # for rating in ratingLike:
    # print(rating)
    # print(rating)
    # print(ratingSave.get(card=1))
    #print(str(rating.get('card'))+" - " + str(rating.get('user')))

    # if ratingSave.filter(Q(card_id=rating.get('card')) & Q(user_id=rating.get('user'))).first():
    # if ratingSave.get(Q(card=rating.get('card')) & Q(user=rating.get('user'))):
    # print("si")

    # Filtrando los usuarios que han visto las películas y guardándolas
    #userSubset = ratings_df[ratings_df['movieId'].isin(inputMovies['movieId'].tolist())]
    # userSubset.head()
    userSubsetLike = ratingLike[ratingLike['card'].isin(
        inputCards['card'].tolist())]
    userSubsetSave = ratingSave[ratingSave['card'].isin(
        inputCards['card'].tolist())]

    # print(userSubsetLike)
    # print("---------------")
    # print(userSubsetSave)

    userSubset = pd.merge(userSubsetLike, userSubsetSave, how='outer', left_on=[
                          'card', 'user'], right_on=['card', 'user'])
    userSubset.drop_duplicates()
    userSubset.to_csv('userSubset.csv')
    userSubset['rating_x'] = userSubset['rating_x'].fillna(0)
    userSubset['rating_y'] = userSubset['rating_y'].fillna(0)

    userSubset["rating"] = userSubset['rating_x'].astype(
        int) + userSubset["rating_y"]

    userSubset = userSubset.drop('rating_x', 1)
    userSubset = userSubset.drop('rating_y', 1)

    # userSubset.to_csv('userSubset.csv')
    # print(userSubset)

    userSubsetRating = pd.merge(ratingLike, ratingSave, how='outer', left_on=[
                                'card', 'user'], right_on=['card', 'user'])
    userSubestRating = userSubsetRating.drop_duplicates()

    userSubsetRating['rating_x'] = userSubsetRating['rating_x'].fillna(0)
    userSubsetRating['rating_y'] = userSubsetRating['rating_y'].fillna(0)
    # userSubsetRating.to_csv('DATA.csv')

    userSubsetRating["rating"] = userSubsetRating['rating_x'].astype(
        int) + userSubsetRating["rating_y"]

    userSubsetRating = userSubsetRating.drop('rating_x', 1)
    userSubsetRating = userSubsetRating.drop('rating_y', 1)

    #pd.DataFrame.to_csv(path_or_buf="/Users/soportecda/Desktop/data", sep=',', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, compression='infer', quoting=None, quotechar='"', line_terminator=None, chunksize=None, date_format=None, doublequote=True, escapechar=None, decimal='.', errors='strict', storage_options=None)
    userSubsetRating.to_csv('DATA.csv')
    # print(userSubsetRating)
    # Groupby crea varios dataframes donde todos tienen el mismo valor para la columna especificada como parámetro
    #userSubsetGroup = userSubset.groupby(['userId'])

    userSubsetGroup = userSubset.groupby(['user'])
    # print(userSubsetGroup)
    # Ordenamiento de forma tal de que los usuarios con más películas en común tengan prioridad
    userSubsetGroup = sorted(
        userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

    #userSubsetGroup = userSubsetGroup[0:100]
    # print(userSubsetGroup)
    # Magia

    # Guardar la Correlación Pearson en un diccionario, donde la clave es el Id del usuario y el valor es el coeficiente
    pearsonCorrelationDict = {}

    # Para cada grupo de usuarios en nuestro subconjunto
    for name, group in userSubsetGroup:
        # print(group)
        # Comencemos ordenando el usuario actual y el ingresado de forma tal que los valores no se mezclen luego
        group = group.sort_values(by='card')

        inputCards = inputCards.sort_values(by='card')

        # Obtener el N para la fórmula
        nRatings = len(group)

        # Obtener los puntajes de revisión para las películas en común
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
            print(Sxx)
            print(Syy)
            print(Sxy)
            print("-")
            pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
        else:
            pearsonCorrelationDict[name] = 0

    pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
    pearsonDF.columns = ['similarityIndex']
    pearsonDF['user'] = pearsonDF.index
    pearsonDF.index = range(len(pearsonDF))
    pearsonDF.head()

    topUsers = pearsonDF.sort_values(
        by='similarityIndex', ascending=False)[0:50]
    topUsers.head()

    topUsersRating = topUsers.merge(
        userSubsetRating, left_on='user', right_on='user', how='inner')
    topUsersRating.head()

    # Se multiplica la similitud de los puntajes de los usuarios
    topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * \
        topUsersRating['rating']
    topUsersRating.head()

    # Se aplica una suma a los topUsers luego de agruparlos por userId
    tempTopUsersRating = topUsersRating.groupby(
        'card').sum()[['similarityIndex', 'weightedRating']]
    tempTopUsersRating.columns = ['sum_similarityIndex', 'sum_weightedRating']
    tempTopUsersRating.head()
    # print(tempTopUsersRating)

    # Se crea un dataframe vacío
    recommendation_df = pd.DataFrame()
    # Ahora se toma el promedio ponderado
    recommendation_df['card'] = tempTopUsersRating.index
    recommendation_df['score'] = tempTopUsersRating['sum_weightedRating'] / \
        tempTopUsersRating['sum_similarityIndex']

    # recommendation_df.head()
    # print(tempTopUsersRating)
    recommendation_df = recommendation_df.sort_values(
        by='score', ascending=False)
    # recommendation_df.head(10)

    recommendation_df = recommendation_df.head(10)

    cardList = Card.objects.filter(
        id__in=recommendation_df.head(10).index).values()

    return list(cardList)
    # return tempTopUsersRating.head(10)
    # return recommendation_df['score'].head(10)
