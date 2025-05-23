from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.context_processors import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import  UpdateView, ListView, DetailView, CreateView

from board.filters import CommentFilter
from board.forms import PostForm, CommentForm
from board.models import User, Post, Comment


class Profile(LoginRequiredMixin, ListView):

    def __init__(self):
        super().__init__()
        self.filterset =None

    model = Comment
    template_name = 'profile.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comment.objects.filter(post__user=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset, request=self.request.user)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


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
            send_mail(
                subject='Отклик на объявление!',
                message=f'Привет! На Ваше объявление "{post.title}" оставлен отклик пользователем "{comment.user}"',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[post.user.email]
            )
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


def comment_accept(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.status = True
    comment.save()
    send_mail(
        subject='Изменение статуса отклика!',
        message=f'Привет! Ваш отклик на объявление "{comment.post.title}..." был принят автором!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[comment.user.email]
    )
    return redirect('/')


def comment_delete(request, pk):
    Comment.objects.get(pk=pk).delete()
    return redirect('/')

""" Проверка команд Git """
""" Проверка команд Git-2 """