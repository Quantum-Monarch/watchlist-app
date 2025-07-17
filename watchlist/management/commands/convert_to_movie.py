from django.core.management.base import BaseCommand
from watchlist.models import Movies
from watchlist.load_data import films

class Command(BaseCommand):
    help = "Convert all existing Film instances into Movies instances"

    def handle(self, *args, **kwargs):
        created_count = 0
        skipped_count = 0

        for film in films:
            if not Movies.objects.filter(pk=film.pk).exists():
                Movies.objects.create(film_ptr_id=film.pk)
                created_count += 1
                self.stdout.write(f"Created Movies instance for Film id={film.pk}")
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done! Created {created_count} Movies instances. Skipped {skipped_count} (already existed)."
        ))
