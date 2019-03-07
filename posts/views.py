from django.shortcuts import render
from posts.models import Blog, Blogger, Comment
from django.views import generic
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin

# Form Imports
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):

    num_blogs = Blog.objects.all().count()
    num_bloggers = Blogger.objects.all().count()

     # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
   
    context = {
       'num_blogs' : num_blogs,
       'num_bloggers' : num_bloggers,
       'num_visits' : num_visits,
    }

    return render(request, 'index.html', context=context )

class BlogListView (generic.ListView):
    model = Blog
    paginate_by = 10
    ordering = ['-post_date']

class BlogDetailView (generic.DetailView):
    model = Blog
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView,self).get_context_data(**kwargs)
        comments_list =  Comment.objects.filter(blog_id = self.kwargs['pk']).order_by('date')

        paginator = Paginator( comments_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)


        context['comments'] = comments
        
        return context


class BloggerListView (generic.ListView):
    model = Blogger
    paginate_by = 10

class BloggerDetailView (generic.DetailView):
    model= Blogger 
    paginate_by = 5 

    def get_context_data(self, **kwargs):
        context = super(BloggerDetailView, self).get_context_data(**kwargs)
        blog_list = Blog.objects.filter(user_id =  self.kwargs['pk'] ).order_by('-post_date')
        paginator = Paginator( blog_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)


        context['blogs'] = blogs
       
        return context

class BlogsByLoggedInUserListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name ='posts/blogs_by_user_loggedIn.html'
    paginate_by = 10

    def get_queryset (self):
        return Blog.objects.filter(user__user = self.request.user)

# FORM VIEWS

class BlogCreate(LoginRequiredMixin,CreateView):
    model = Blog
    fields = ['title','content']
    
    def form_valid(self,form):
        
        form.instance.user = Blogger.objects.get(user = self.request.user )

        return super(BlogCreate, self).form_valid(form)

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.user = Blogger.objects.get(user = self.request.user )
    #     obj.save()
    #     return HttpResponseRedirect(obj.get_absolute_url())

class BlogUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'content']

    def test_func(self):
        obj  = self.get_object()
        return obj.user.user == self.request.user

class BlogDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('index')

    def get_success_url(self, **kwargs):
        return self.request.GET.get('next', reverse_lazy('index'))

    def test_func(self):
        obj  = self.get_object()
        return obj.user.user == self.request.user

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment',]

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog-detail', kwargs = { 'pk' : self.kwargs['pk'] })

    def form_valid(self,form):

        form.instance.user = Blogger.objects.get(user = self.request.user )

        form.instance.blog = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return super(CommentCreate, self).form_valid(form)
    


    
    