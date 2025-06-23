from django import forms

from .models import Movies, Series, UserList, UserListItem


class UserListItemForm(forms.ModelForm):
    class Meta:
        model = UserListItem
        fields = ['rating','status']

class UserListItemFormS(forms.ModelForm):
    class Meta:
        model =UserListItem
        fields = ['rating','status','current_episode']
class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['name','release_year']


class AddSeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name','release_year','number_of_episodes','number_of_seasons','next_release_date']

class MakePublic(forms.ModelForm):
    class Meta:
        model = UserList
        fields=['name']
