from django.contrib import admin
from .models import Movies, Series, UserList


class MoviesAdmin(admin.ModelAdmin):
    list_display=('name','release_year','status','rating','movie_length')
    list_filter=('release_year',)
    search_fields=('name','status')
class SeriesAdmin(admin.ModelAdmin):
    list_display=('name','release_year','status','rating','current_episode')
    list_filter=('release_year',)
    search_fields=('name','status')
class UserListAdmin(admin.ModelAdmin):
    list_display=('name','user','ispublic')
admin.site.register(UserList,UserListAdmin)
admin.site.register(Movies,MoviesAdmin)
admin.site.register(Series,SeriesAdmin)