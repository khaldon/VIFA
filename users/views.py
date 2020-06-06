from django.views.generic import CreateView,TemplateView
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .models import CustomUser, Profile
from django.conf import settings
from .forms import SignUpForm


# Create a user instance from Auth_USER_MODEL
User = settings.AUTH_USER_MODEL

# Home page view 
def home(request):
    return render(request, 'home.html' )



# Create user profile 
def profile(request):
    pass 




# Create a signup view 
class Signup(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'


    def form_valid(self, form):
        user = form.save()
        auth_login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('users:login')


# Delete a user instance 
def delete_user(request, username):
    u = CustomUser.objects.get(username=username)
    u.delete()
    return redirect('core:home')
    