from django.contrib import admin
from .models import Movies, Series, UserList, UserListItem


class MoviesAdmin(admin.ModelAdmin):
    list_display=('name','release_year','movie_length')
    list_filter=('release_year',)
class SeriesAdmin(admin.ModelAdmin):
    list_display=('name','release_year')
    list_filter=('release_year',)
class UserListAdmin(admin.ModelAdmin):
    list_display=('name','user','ispublic')
class UserListItemAdmin(admin.ModelAdmin):
    list_display=('userlist','film')
admin.site.register(UserListItem, UserListItemAdmin)
admin.site.register(UserList,UserListAdmin)
admin.site.register(Movies,MoviesAdmin)
admin.site.register(Series,SeriesAdmin)