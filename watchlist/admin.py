from django.contrib import admin
from .models import Movies,Series

class MoviesAdmin(admin.ModelAdmin):
    list_display=('name','release_year','status','rating','movie_length')
    list_filter=('release_year',)
    search_fields=('name','status')
class SeriesAdmin(admin.ModelAdmin):
    list_display=('name','release_year','status','rating','current_episode')
    list_filter=('release_year',)
    search_fields=('name','status')
admin.site.register(Movies,MoviesAdmin)
admin.site.register(Series,SeriesAdmin)