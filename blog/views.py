from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm, UserCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # For CBV
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)

from braces.views import SelectRelatedMixin
# Create your views here.

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'blog/signup.html'

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self): # Instead of getting all rows, we are filtering here
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, SelectRelatedMixin, CreateView):
    login_url = '/account/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        print("working...")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/account/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/account/login/'
    model = Post
    success_url = reverse_lazy('post_list') # reverse_lazy make sure that post is deleted, then redirect.

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    redirect_field_name = 'blog/post_list.html'
    template_name = 'post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, author=self.request.user).order_by('created_date')

### publish the post ###
@login_required(login_url="/account/login/")
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


#### comment section ####
@login_required(login_url="/account/login/")
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post           # ForeignKey relation. "commit.post" from Comment model and "post" from first line of this function
            comment.author = request.user # ie; connecting this comment to that post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required(login_url="/account/login/")
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()  # user defined method. check Comment model.
    return redirect('post_detail', pk=comment.post.pk) # pk of post

@login_required(login_url="/account/login/")
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
