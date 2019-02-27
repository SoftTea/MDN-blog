from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

# Create your models here.

class Blogger(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)

    biography = models.TextField(max_length = 1000, help_text='Biography for blogger info')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger-detail' , args=[str(self.id)])

class Blog(models.Model):

    title = models.CharField(max_length = 200)

    user = models.ForeignKey('Blogger', on_delete=models.CASCADE)

    post_date = models.DateField(auto_now = True)

    content = models.TextField()

    class Meta: 
        ordering = ['user' , 'post_date' , 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail' , args=[str(self.id)])

class Comment(models.Model): 

    user = models.ForeignKey('Blogger', on_delete = models.CASCADE )

    date = models.DateField(auto_now= True)

    comment = models.TextField()

    blog = models.ForeignKey('Blog' , on_delete= models.CASCADE )

    class Meta: 
        ordering = ['blog' , 'date']

    def __str__(self):
        return f'{self.user}'



