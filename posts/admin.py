from django.contrib import admin
from posts.models import Blogger, Blog, Comment

# Register your models here.

admin.site.register(Blogger)
admin.site.register(Blog)
admin.site.register(Comment)