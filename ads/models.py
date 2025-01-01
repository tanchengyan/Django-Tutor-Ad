from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
# Default User model
from django.contrib.auth.models import User


from datetime import timedelta

# Create your models here.
# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=100)
 
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from category name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
# Author Model
class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(default="default-profile-pic.png", upload_to='uploads/profile-pictures', null=True)
    preferred_name = models.CharField(max_length=200, blank=True, null=True)
    tel_number = models.CharField(max_length=200, blank=True, null=True)
    wechat = models.CharField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.user.username

# Tutor Ad Model
class TutorAd(models.Model):

    # Link to Author (Tutor)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    
    # Ad-specific details
    title = models.CharField(max_length=200)
    about_tutor = models.TextField()  # New field: Details about the tutor
    about_lesson = models.TextField()  # New field: Details about the lesson
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tutor_ads',default=2)

    subject = models.CharField(max_length=200)  # The subject of the lesson (e.g., "GRE", "Computer Science")
    rate = models.DecimalField(max_digits=8, decimal_places=0)  # Hourly rate
    
    last_time_active = models.DateTimeField(auto_now=True)  # Automatically updated when tutor is active
    average_response_time = models.DurationField(default=timedelta(hours=1))  # Average response time to inquiries
    
    #preffered contact method
    contact_tel = models.BooleanField(default=False)
    contact_email = models.BooleanField(default=False)
    contact_wechat = models.BooleanField(default=False)
    

    
    # Additional details (video or images)
   
    is_featured = models.BooleanField(default=False)  # Mark as featured
    is_active = models.BooleanField(default=True)  # Ad status

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author.user.username}"

    class Meta:
        verbose_name_plural = "Tutor Ads"

# Review Model
    




# Image Model
class AdsImages(models.Model):
    ads = models.ForeignKey(TutorAd, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', default=None)

    def __str__(self):
        return self.ads.title

    class Meta:
        verbose_name_plural = 'Classified Ads Images'


#         return self.title

    



    
    

