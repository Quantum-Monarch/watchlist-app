from django import forms

from .models import  UserList, UserListItem


class UserListItemForm(forms.ModelForm):
    class Meta:
        model = UserListItem
        fields = ['rating','status']

class UserListItemFormS(forms.ModelForm):
    class Meta:
        model =UserListItem
        fields = ['rating','status','current_episode']

class MakePublic(forms.ModelForm):
    class Meta:
        model = UserList
        fields=['name']
