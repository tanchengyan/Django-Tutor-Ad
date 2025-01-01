from django.forms import ModelForm
# importing default user registration form
from django.contrib.auth.forms import UserCreationForm
# importing built-in user model
from django.contrib.auth.forms import User
from django import forms
from ads.models import Author

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class UserRegistrationForm(UserCreationForm):
    # Styling the username form fields
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'username', 
        'placeholder': 'Username'
    }))

    # Styling the password1 form fields
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'password1', 
        'placeholder': 'Password'
    }))

    # Styling the password2 form fields
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'password2', 
        'placeholder': 'Retype Password'
    }))
    
    # Making the email field required 
    email = forms.EmailField(required=True)

    # Styling the email form fields
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control',  
        'placeholder': 'Email Address'
    }))

    preferred_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'preferred_name',
        'placeholder': 'Preferred Name (Optional)'
    }))

    
    
    class Meta:
        model = User
        fields = ['username', 'preferred_name','email','password1','password2']


    def clean_email(self):
        email = self.cleaned_data['email']
        duplicate_email = User.objects.filter(email=email).exists()
        print("Email Taken")
        if duplicate_email:
            raise forms.ValidationError("This Email address is already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            preferred_name = self.cleaned_data.get('preferred_name')
            author = Author.objects.create(user=user)
            if preferred_name:
                author.preferred_name = preferred_name
            else:
                author.preferred_name = user.username
            author.save()
        return user

class EmailValidationOnForgotPassword(PasswordResetForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control',  
        'placeholder': 'Email Address'
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")

        return email

class EmailSetPassword(SetPasswordForm):
    # Styling the password1 form fields
    new_password1 = forms.CharField(label="", widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'new_password1', 
        'placeholder': 'Password'
    }))

    # Styling the password2 form fields
    new_password2 = forms.CharField(label="", widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'new_password2', 
        'placeholder': 'Retype Password'
    }))

# Updating the User registration form
class UserUpdateForm(ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'first_name', 
        'placeholder': 'First Name'
    }))

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'last_name', 
        'placeholder': 'Last Name'
    }))

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control',  
        'placeholder': 'Email Address'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # exclude = ['user']

# Updating the profile form
class ProfileUpdateForm(ModelForm):
    preferred_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'preferred_name',
        'placeholder': 'Preferred Name'
    }))

    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'phone_number',
        'placeholder': 'Phone Number'
    }))
    linkedin_url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'name': 'linkedin_url',
        'placeholder': 'LinkedIn URL'
    }))
    wechat = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'wechat',
        'placeholder': 'WeChat ID'
    }))

    

    class Meta:
        model = Author
        fields = ['preferred_name', 'phone_number', 'linkedin_url', 'wechat']
        