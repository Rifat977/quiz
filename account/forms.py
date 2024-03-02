from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, error_messages={'required': _('Email field is required.')})
    first_name = forms.CharField(max_length=30, required=True, error_messages={'required': _('First name field is required.')})
    last_name = forms.CharField(max_length=30, required=True, error_messages={'required': _('Last name field is required.')})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': _('Username field is required.'),
            },
            'password1': {
                'required': _('Password field is required.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].error_messages = {'required': _('Password field is required.')}
        self.fields['password2'].error_messages = {'required': _('Password confirmation field is required.')}


    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    identifier = forms.CharField(label="Username or Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
