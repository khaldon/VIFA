from django.views.generic import CreateView,TemplateView
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .models import CustomUser, Profile
from django.conf import settings
from .forms import SignUpForm, UserEditForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

# Create a user instance from Auth_USER_MODEL
User = settings.AUTH_USER_MODEL

# Home page view 
def home(request):
    return render(request, 'home.html' )



# Create user profile 
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated')
        else:
            messages.error(request, 'Please correct that errors in your profile form.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'user_form':user_form,'profile_form':profile_form})

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
    