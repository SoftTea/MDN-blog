from django import forms

from django.forms import ModelForm

from posts.models import Blog

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class CreateBlogModelForm (ModelForm):
#     class Meta: 
#         model = Blog
#         include = '__all__'

class SignUpForm(UserCreationForm):
    biography = forms.CharField(widget=forms.Textarea , help_text='Short biographical profile - Optional', max_length = 1000 , required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'biography' )