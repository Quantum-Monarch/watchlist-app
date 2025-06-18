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