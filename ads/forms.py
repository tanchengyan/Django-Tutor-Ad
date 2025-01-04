from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import *
from django.utils.html import format_html
from django.urls import reverse

class PostAdsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',
        'name': 'title',
        'placeholder': 'Title'
    }))

    about_tutor = forms.CharField(widget=CKEditor5Widget(attrs={
        'type': 'text',
        'class': 'form-control',
        'name': 'about_tutor',
        'placeholder': 'About the tutor'
    }))

    about_lesson = forms.CharField(widget=CKEditor5Widget(attrs={
        'type': 'text',
        'class': 'form-control',
        'name': 'about_lesson',
        'placeholder': 'About the lesson'
    }))

    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'name': 'category',
        'placeholder': 'Select Category'
    }))

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',
        'name': 'subject',
        'placeholder': 'Subject'
    }))

    rate = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'name': 'rate',
        'placeholder': 'Hourly Rate'
    }))



    class Meta:
        model = TutorAd
        fields = ['title', 'about_tutor', 'about_lesson', 'category', 'subject', 'rate', 'contact_tel', 'contact_email', 'contact_wechat']
        exclude = ['author', 'last_time_active', 'average_response_time', 'number_of_students', 'date_created','is_featured', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'about_tutor': forms.Textarea(attrs={'class': 'form-control'}),
            'about_lesson': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_tel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contact_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contact_wechat': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        contact_tel = cleaned_data.get('contact_tel')
        contact_email = cleaned_data.get('contact_email')
        contact_wechat = cleaned_data.get('contact_wechat')
        author = self.user.author


        profile_settings_url = reverse('profile-settings')

        if contact_tel and not author.tel_number:
            self.add_error('contact_tel', format_html('You selected contact by phone, but no phone number is provided in your profile settings. Please update your <a href="{}">Profile Settings</a>.', profile_settings_url))
        if contact_email and not author.user.email:
            self.add_error('contact_email', 'You selected contact by email, but no email address is provided in your profile settings.')
        if contact_wechat and not author.wechat:
           self.add_error('contact_wechat', format_html('You selected contact by WeChat, but no WeChat ID is provided in your profile settings. Please update your <a href="{}">Profile Settings</a>.', profile_settings_url))

        return cleaned_data
    

class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'placeholder': 'Enter keywords'
    }), required=False)
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        required=False
    )

class AdsImagesForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)

    class Meta:
        model = AdsImages
        fields = ['images']
    
    def clean_images(self):
        images = self.files.getlist('images')
        if len(images) > 5:
            raise forms.ValidationError("You can upload a maximum of 5 images.")
        return images