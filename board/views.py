
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView, ListView, DetailView, CreateView

from board.forms import PostForm, CommentForm
from board.models import User, Post, Comment


class Profile(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'profile.html')


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code = request.POST.get('code')
            user = User.objects.filter(code=code)
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)

            return redirect('account_login')


class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context



    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = self.request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
        return self.render_to_response(self.get_context_data(form=form, post=post))



class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


