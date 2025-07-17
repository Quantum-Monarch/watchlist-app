import pandas as pd
from django.shortcuts import render
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from .models import UserPreferences,Film
films=Film.objects.all().order_by('id')
def add_to_selection(top_selection,score,tmdbid):
    if len(top_selection) < 5:
        top_selection[tmdbid] = score
    elif len(top_selection) < 5:
        lowest_id, lowest_score = min(top_selection.items(), key=lambda x: x[1])
        if score > lowest_score:
            del top_selection[lowest_id]
            top_selection[tmdbid] = score
    return top_selection

def filtersearch():
    qst=films.filter(tmdb_rating__gt=5)
    df = pd.DataFrame(list(qst.values('tmdb_id', 'main_vector', 'tmdb_rating')))
    return df

def calculate_similarity(df,usergenrevector):
    if not usergenrevector :
        return df
    else:
        uvec = np.array(usergenrevector).reshape(1, -1)
        matrix = np.stack(df['main_vector'].values)
        similarities = cosine_similarity(uvec, matrix)[0]
        df['alignment'] = similarities
        df=df[df['alignment']>=0.5].copy()
        return df
    #filter on cosine similarity cap use pandas to return dataframe with cosine similarity results
def score_select_top5(df):
    if 'alignment' not in df.columns:
        df.drop(['main_vector'], axis=1, inplace=True)
        top_selection = {}
        for item in df.itertuples():
            add_to_selection(top_selection, item.tmdb_rating, item.tmdb_id)
        return top_selection
    else:
        df['score']=df['alignment']*df['main_vector'].apply(lambda v: np.linalg.norm(v))
        df.drop(['alignment','main_vector','tmdb_rating'],axis=1,inplace=True)
        top_selection = {}
        for item in df.itertuples():
            top_selection=add_to_selection(top_selection, item.score, item.tmdb_id)
        return top_selection
    #cosism results*magnitude of filmvector, use dict to keep track of top 5 scores
def recommend(usergenrevector,df):
    k=filtersearch()
    b=calculate_similarity(k, usergenrevector)
    top_selection=score_select_top5(b)
    return top_selection
