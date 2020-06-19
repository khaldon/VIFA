from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.conf import settings
from django.forms.widgets import ClearableFileInput

# Create a user instance 
User = settings.AUTH_USER_MODEL


# Create custom file input for upload image profile page
class CustomClearableFileInput(ClearableFileInput):
    template_name = 'users/custom_clear_file_input.html'


# create a sign up form 
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['username'].widget.attrs.update({'placeholder': 'username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'email'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


# Create a custom edit form 
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


# create a custom user form 
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].widget.attrs.update({'placeholder': 'password'})


# user a email instead of the default username 
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('birth_date', 'gender', 'country', 'city', 'bio', 'image')
        widgets = {
            'image': CustomClearableFileInput(),
         }
