from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):

    name = models.CharField(max_length=100)
    release_year = models.IntegerField(default=1999)
    tmdb_id=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.name
    def get_release_year(self):
        return self.release_year

class Movies(Film):
    movie_length=models.IntegerField(default=0)
    def get_movie_length(self):
        return self.movie_length

class Series(Film):
    upcoming_CHOICES = [
        ("unknown", "to be determined"),
        ("completed", "finished airing"),
    ]

    number_of_seasons = models.IntegerField(default=2)
    number_of_episodes = models.IntegerField(default=20)
    next_release_date=models.CharField(choices=upcoming_CHOICES,max_length=100 ,default="unknown")
    def get_next_release_date(self):
        return self.next_release_date
    def get_current_episode(self):
        return self.current_episode
    def get_number_of_seasons(self):
        return self.number_of_seasons
    def get_number_of_episodes(self):
        return self.number_of_episodes
class UserList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ispublic = models.BooleanField(default=False)
    name = models.CharField(max_length=100)

class UserListItem(models.Model):
    Status_CHOICES = [
        ("null","not set"),
        ("plan", "planned to watch"),
        ("watched", "watched"),
        ("watching", "watching"),
    ]
    userlist = models.ForeignKey(UserList,related_name='items', on_delete=models.CASCADE,null=True,blank=True)
    film=models.ForeignKey(Film,on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=Status_CHOICES, default="null")
    rating = models.FloatField(default=0.0)
    added_on = models.DateTimeField(auto_now_add=True)
    current_episode = models.IntegerField(default=0,null=True,blank=True)
    def get_status(self):
        return self.status
    def get_rating(self):
        return self.rating



