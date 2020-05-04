from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	DeleteView,
	UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
def home(request):
	posts = Post.objects.all()
	context = {'posts': posts}
	return render(request, 'blog/home.html', context)

def about(request):
	return render(request, 'blog/about.html')

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' #template_name = <app>/<model>_<viewtype>.html by default
	context_object_name = 'posts' 
	ordering = ['-date_posted']
	paginate_by = 5 #class attribute that sets how many objects per page

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_post.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	'''
	if form is valid, then the author of that instance of form is set to the current request.user
	'''
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	'''
	if form is valid, then the author of that instance of form is set to the current request.user
	'''
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	'''
	UserPassesTestMixin required function to test if the user can update the form.
	Prevents other users to update a user's posts.
	'''
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	'''
	UserPassesTestMixin required function to test if the user can update the form.
	Prevents other users to update a user's posts.
	'''
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
