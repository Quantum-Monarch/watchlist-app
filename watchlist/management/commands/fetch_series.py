import requests
from django.core.management.base import BaseCommand
from watchlist.models import Film, Movies, Series
import logging
import time

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch movies from TMDb and populate Series(and Film) table'

    def handle(self, *args, **kwargs):
        api_key = '25aa714aea84f2d0a638430e5c1dd346'
        total_api_calls = 0
        max_api_calls = 1000  # TMDB free plan daily limit
        created_count = 0
        updated_count = 0
        failed_count = 0

        page = 1
        while total_api_calls < max_api_calls:
            url = f'https://api.themoviedb.org/3/tv/popular?api_key={api_key}&language=en-US&page={page}'
            response = requests.get(url)
            total_api_calls += 1

            if response.status_code != 200:
                logger.error(f"Failed to fetch page {page}: {response.text}")
                break

            data = response.json()
            movies = data.get('results', [])
            if not movies:
                logger.info("No more movies to process.")
                break

            for movie in movies:
                if  movie['id'] in Film.objects.all():
                    self.stdout.write(f"skipped series instance for Film id={movie['id']}")
                    continue
                else:
                    if total_api_calls >= max_api_calls:
                        logger.warning("API daily limit reached — stopping.")
                        break

                    tmdb_id = movie['id']
                    name = movie['name']
                    release_year = int(movie['release_date'][:4]) if movie.get('release_date') else 1999
                    rating = int(movie.get('vote_average', 0))
                # Fetch details

                    details_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}&language=en-US'
                    details_resp = requests.get(details_url)
                    total_api_calls += 1
                    time.sleep(0.3)

                    if details_resp.status_code != 200:
                        logger.warning(f"Failed to fetch details for {tmdb_id}")
                        failed_count += 1
                        continue

                    details = details_resp.json()
                    genres = [g['name'].lower() for g in details.get('genres', [])]
                    companies = [c['name'].lower() for c in details.get('production_companies', [])]
                    poster_path = details.get('poster_path')
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                    number_of_seasons = details.get('number_of_seasons', 0)
                    number_of_episodes = details.get('number_of_episodes', 0)

                    series, created = Series.objects.update_or_create(
                        tmdb_id=tmdb_id,
                        defaults={
                            'name': name,
                            'release_year': release_year,
                            'tmdb_rating': rating,
                            'genre': genres,
                            'production_company': companies,
                            'poster_url': poster_url,
                            'number_of_seasons': number_of_seasons,
                            'number_of_episodes': number_of_episodes,
                        }
                    )
                    series.create_main_vector()
                    if created:
                        created_count += 1
                        self.stdout.write(f"Created Movies instance for Film id={series.pk}")
                        logger.info(f"Created film: {name}")
                    else:
                        updated_count += 1
                        logger.info(f"Updated film: {name}")

                    # be nice to the API
                    time.sleep(0.3)

            if total_api_calls >= max_api_calls:
                logger.warning("API daily limit reached — stopping.")
                break

            page += 1

        # Print summary
        logger.info("========== SUMMARY ==========")
        logger.info(f"Created: {created_count}")
        logger.info(f"Updated: {updated_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"API calls used: {total_api_calls}")
        logger.info("=============================")

        if created_count + updated_count > 0:
            self.stdout.write(self.style.SUCCESS("✅ Movie fetching completed successfully!"))
        else:
            self.stdout.write(self.style.ERROR("⚠️ No movies were created or updated."))
