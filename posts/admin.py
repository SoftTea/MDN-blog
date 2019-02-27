from django.contrib import admin
from posts.models import Blogger, Blog, Comment
from django.contrib.auth.models import User

# Register your models here.

# admin.site.register(Blogger)
# admin.site.register(Blog)
# admin.site.register(Comment)

class CommentsInstanceInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('user','date','comment')
    extra = 0
    show_change_link = True




@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):

    def user_email(self,obj):
       return obj.user.email
    user_email.short_description = 'Email'

    def date_joined(self,obj):
       return obj.user.date_joined
    date_joined.short_description = 'date joined'
    
    list_display = ('user', 'user_email', 'date_joined',)
    

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    

    list_display = ('title' ,'user' , 'post_date')
    list_filter = ('user',)
    readonly_fields = ('post_date',)
    inlines= [CommentsInstanceInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'date')
    list_filter = ('blog',)
    readonly_fields = ('date',)
