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
            'release_year' :tmdb_movie_data['release_date'][:4] if tmdb_movie_data['release_date'] else None
        }
    )
    user_list, created=UserList.objects.get_or_create(
        user=user_id,
        defaults={'ispublic': False, 'name': 'My Watchlist'}

    )
    userlistitem,created= UserListItem.objects.get_or_create(
        film=movie,
        defaults={
            'userlist':user_list,
            'rating': tmdb_movie_data['vote_average'],
            'status': 'not set'
        }
    )
    return userlistitem