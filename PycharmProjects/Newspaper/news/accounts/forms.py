from django import forms
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']

class BecomeAuthorForm(forms.Form):
    confirm = forms.BooleanField(
        label="Я подтверждаю, что хочу стать автором и согласен с правилами",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )