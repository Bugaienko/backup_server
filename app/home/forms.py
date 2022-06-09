import datetime
from datetime import date, timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import CustomUser, Questions


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username',
        )


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'img',
            'birthday',
            'discount',

        )


class QuestionsForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Questions
        fields = ("name", "email", "text")


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
        )


class CustomUserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'img',
            'birthday',
        )
        # birthday = forms.DateField(forms.SelectDateWidget())
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(1922, 2023)),

        }
