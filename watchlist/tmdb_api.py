from rest_framework.generics import get_object_or_404

from .models import Movies, UserListItem, Film, UserList
import requests

TMDB_API_KEY = '25aa714aea84f2d0a638430e5c1dd346'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
def search_movies(query,page=1):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'page': page,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results')
    else:
        return []


def get_movie_details_from_tmdb(tmdb_id):
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_tmdb_movie(tmdb_movie_data,user_id):
    movie, created = Movies.objects.get_or_create(
        tmdb_id=tmdb_movie_data['id'],
        defaults={
            'name' :tmdb_movie_data['title'],
            'release_year' :int(tmdb_movie_data['release_date'][:4]) if tmdb_movie_data['release_date'] else None,
            'genre' :[g["name"] for g in tmdb_movie_data.get("genres",[])],
            'production_company' :[p["name"] for p in tmdb_movie_data.get("production_companies",[])],
            'tmdb_rating' :int(tmdb_movie_data.get('vote_average', 0)),
            'poster_url' :tmdb_movie_data.get('poster_path'),
        }
    )
    if created:
        movie.create_main_vector()


    user_list, created=UserList.objects.get_or_create(
        user=user_id.id,
        defaults={'ispublic': False, 'name': 'My Watchlist'}

    )
    film=get_object_or_404(Film, tmdb_id=tmdb_movie_data['id'])
    userlistitem,created= UserListItem.objects.get_or_create(
        film=film,
        defaults={
            'userlist':user_list,
            'rating': tmdb_movie_data['vote_average'],
            'status': 'not set'
        }
    )
    return film