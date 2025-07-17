from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
import numpy as np

class Film(models.Model):
    name = models.CharField(max_length=100)
    release_year = models.IntegerField(default=1999)
    tmdb_id=models.IntegerField(null=True,blank=True)
    genre=ArrayField(models.CharField(),default=list)
    production_company=ArrayField(models.CharField(),default=list,null=True)
    tmdb_rating=models.IntegerField(default=0,null=True,blank=True)
    main_vector=ArrayField(models.IntegerField(),default=list,null=True)
    poster_url=models.URLField(null=True,blank=True)
    def create_main_vector(self):
        genre_vector=[0]*11
        company_vector=[0]*10
        companydic = {
            "warner bros.": 0,
            "universal pictures": 1,
            "paramount pictures": 2,
            "walt disney pictures": 3,
            "20th century fox": 4,
            "columbia pictures": 5,
            "lionsgate": 6,
            "metro-goldwyn-mayer": 7,
            "new line cinema": 8,
        }
        genredic={
            'action':0,
            'adventure':1,
            'drama':2,
            'comedy':3,
            'horror':4,
            'romance':5,
            'sci-fi':6,
            'documentary':7,
            'animation':8,
            'crime':9,
        }
        genre_list = [g for g in self.genre]
        for genre in genre_list:
            if genre not in genredic:
                genre_vector[10]=1
            else:
                genre_vector[genredic[genre]]=1

        company_list=[g for g in self.production_company]
        for company in company_list:
            if company not in companydic:
                company_vector[9]=1
            else:
                company_vector[companydic[company]]=1

        self.main_vector=genre_vector+company_vector
        self.save()
    def __str__(self):
        return self.name
    def get_release_year(self):
        return self.release_year

class Movies(Film):
    movie_length=models.IntegerField(default=0)
    def get_movie_length(self):
        return self.movie_length

class Series(Film):
    number_of_seasons = models.IntegerField(default=2)
    number_of_episodes = models.IntegerField(default=20)
    def get_number_of_seasons(self):
        return self.number_of_seasons
    def get_number_of_episodes(self):
        return self.number_of_episodes

class UserList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    ispublic = models.BooleanField(default=False)
    name = models.CharField(max_length=100)

class UserListItem(models.Model):
    Status_CHOICES = [
        ("null","not set"),
        ("plan", "planned to watch"),
        ("watched", "watched"),
        ("watching", "watching"),
    ]
    userlist = models.ForeignKey(UserList,related_name='items',on_delete=models.CASCADE,null=True)
    film=models.ForeignKey(Film,on_delete=models.CASCADE)
    rating=models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=Status_CHOICES, default="null")
    rating = models.FloatField(default=0.0)
    added_on = models.DateTimeField(auto_now_add=True)
    current_episode = models.IntegerField(default=0,null=True,blank=True)
    def get_status(self):
        return self.status
    def get_rating(self):
        return self.rating

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    main_vector = ArrayField(models.FloatField(), default=list,null=True)
    def edit_main_vector(self,filmvector):
        if self.main_vector==[]:
            self.main_vector=filmvector
            self.save()
        else:
            newvec=np.array(filmvector)+np.array(self.main_vector)
            self.main_vector = newvec.tolist()
            self.save()
    def edit_main_vector_remove(self,filmvector):
        newvec=np.array(self.main_vector)-np.array(filmvector)
        self.main_vector = newvec.tolist()
        self.save()






