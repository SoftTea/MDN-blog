from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User


# Create your models here.

class Blogger(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)

    biography = models.TextField(max_length = 1000, help_text='Biography for blogger info')

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger-detail' , args=[str(self.id)])

class Blog(models.Model):

    title = models.CharField(max_length = 200)

    user = models.ForeignKey('Blogger', verbose_name = 'Author', on_delete=models.CASCADE)

    post_date = models.DateTimeField(auto_now = True)

    content = models.TextField()

    class Meta: 
        ordering = ['user' , '-post_date' , 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail' , args=[str(self.id)])

class Comment(models.Model): 

    user = models.ForeignKey('Blogger', on_delete = models.CASCADE )

    date = models.DateTimeField(auto_now= True, verbose_name='Comment date')

    comment = models.TextField()

    blog = models.ForeignKey('Blog' , on_delete= models.CASCADE, verbose_name='Comment made on post titled' )

    class Meta: 
        ordering = ['blog' , 'date']

    def get_absolute_url(self):
        return reverse('blog-detail' , args=[str(self.blog.id)])

    def __str__(self):
        return f'{self.user}'



