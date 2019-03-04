from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogs/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('bloggers/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail' ),
    path('myblog', views.BlogsByLoggedInUserListView.as_view(), name='my-blog'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', views.BlogUpdate.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', views.BlogDelete.as_view(), name='blog-delete'),
    path('blogs/<int:pk>/create-comment', views.CommentCreate.as_view(), name='comment-create')
    
]