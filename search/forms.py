from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SearchForm(forms.Form):

    title = forms.CharField(
        initial='',
        label='タイトル',
        required = False, # 必須ではない
    )
    text = forms.CharField(
        initial='',
        label='内容',
        required=False,  # 必須ではない
    )