from django.contrib.auth import forms
from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
    Status_CHOICES = [
        ("null","not set"),
        ("plan", "planned to watch"),
        ("watched", "watched"),
        ("watching", "watching"),
    ]
    name = models.CharField(max_length=100)
    release_year = models.IntegerField(default=1999)
    status=models.CharField(max_length=100,choices=Status_CHOICES)
    rating=models.FloatField(default=0)
    def __str__(self):
        return self.name
    def get_release_year(self):
        return self.release_year
    def get_status(self):
        return self.status
    def get_rating(self):
        return self.rating

class Movies(Film):
    movie_length=models.IntegerField(default=0)
    def get_movie_length(self):
        return self.movie_length

class Series(Film):
    upcoming_CHOICES = [
        ("unknown", "to be determined"),
        ("completed", "finished airing"),
    ]
    current_episode=models.IntegerField()
    number_of_seasons = models.IntegerField()
    number_of_episodes = models.IntegerField()
    next_release_date=models.CharField(choices=upcoming_CHOICES,max_length=100)
    def get_next_release_date(self):
        return self.next_release_date
    def get_current_episode(self):
        return self.current_episode
    def get_number_of_seasons(self):
        return self.number_of_seasons
    def get_number_of_episodes(self):
        return self.number_of_episodes

class UserListItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    film=models.ForeignKey(Film,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

