from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect


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
