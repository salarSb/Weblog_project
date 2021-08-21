from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('articles:articles-list')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
        'page_title': 'Signup'
    }
    return render(request, 'accounts/signup.html', context)


class Login(LoginView):
    extra_context = {
        'page_title': 'Login'
    }


class Logout(LogoutView):
    pass


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ('first_name', 'last_name', 'email')
    success_url = reverse_lazy('articles:articles-list')
    extra_context = {
        'page_title': 'Edit Profile'
    }

    def get_object(self, queryset=None):
        return self.request.user
