from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Cars, Rating, Comment
from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    username = forms.EmailField(label='Email', max_length=255)

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = user.username
        user.save()
        return user


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'mark', 'text', 'post_type', 'short_text']
        labels = {
            'name': _('Nazwa posta'),
            'mark': _('Marka samochodu'),
            'short_text': _('Krótki opis'),
            'text': _('Tekst'),
            'post_type': _('Typ posta')
        }
        widgets = {
            "text": forms.Textarea
        }


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['mark', 'model', 'generation', 'type_of_car', 'fuel', 'engine', 'combustion', 'drive']
        labels = {
            'mark': _('Marka samochodu'),
            'model': _('Model samochodu'),
            'generation': _('Generacja samochodu'),
            'type_of_car': _('Typ samochodu'),
            'fuel': _('Rodzaj paliwa'),
            'engine': _('Pojemność silnika w cc'),
            'combustion': _('Ilość spalanych litrów na 100km'),
            'drive': _('Napęd')
        }


class RateCarsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [ 'look', 'price', 'reliability', 'practicality', 'family_car']
        labels = {
            'look': _('Jak oceniasz wygląd wybranego samochodu?'),
            'price': _('Jak oceniasz cenę tego samochodu?'),
            'reliability': _('Jak oceniasz niezawodność tego samochodu?'),
            'practicality': _('Jak oceniasz praktyczność tego samochodu?'),
            'family_car': _('Jak oceniasz ten samochód pod względem rodzinnym?'),
        }


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': _('Wpisz swój komentarz')
        }

