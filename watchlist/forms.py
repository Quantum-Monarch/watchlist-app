from django import forms

from .models import Movies, Series


class UserListItemForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['rating','status']
class UserListItemFormS(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['rating','status','current_episode']
class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['name','release_year','rating','status']


class AddSeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name','release_year','rating','status','number_of_episodes','number_of_seasons','next_release_date']