
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView
from board.models import User


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

