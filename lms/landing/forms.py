# landing/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',   # critical for Bootstrap
            'placeholder': 'Enter your username',
            'style': 'display:block;width:100%;padding:.375rem .75rem;font-size:1rem;line-height:1.5;color:#212529;background-color:#fff;border:1px solid #ced4da;border-radius:.375rem;',
            'autocomplete': 'off',
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'style': 'display:block;width:100%;padding:.375rem .75rem;font-size:1rem;line-height:1.5;color:#212529;background-color:#fff;border:1px solid #ced4da;border-radius:.375rem;',
            'autocomplete': 'new-password',
        })
    )
