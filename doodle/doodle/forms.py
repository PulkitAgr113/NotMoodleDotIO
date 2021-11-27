from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from chats.models import Score

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        if commit:
            user.save()
            Score.objects.create(user=user)

        return user
