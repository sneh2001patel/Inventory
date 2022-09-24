from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView

from .forms import RegisterForm, LoginForm


# Create your views here.


# def register(response):
#     if response.method == "POST":
#         form = RegisterForm(response.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = RegisterForm()
#     content = {"form": form}
#     return render(response, "authencation/register.html", content)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "authencation/register.html"
    success_url = "/login/"


class LoginView(FormView):
    form_class = LoginForm
    template_name = "authencation/login.html"
    success_url = "/"

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")

        return super(LoginView, self).form_invalid(form)


def costum_logout(request):
    return LogoutView.as_view(template_name='authencation/logout.html')(request)

# def login(response):
#     if response.method == "POST":
#         form = LoginForm(response.POST)
#     #     if form.is_valid():
#     #         # form.save()
#     # else:
#         form = LoginForm()
#     content = {"form": form}
#     return render(response, "authencation/login.html", content)
