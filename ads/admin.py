from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

class AdsImagesAdmin(admin.StackedInline):
    model = AdsImages

class AdsAdmin(admin.ModelAdmin):
    

    # Display columns in the admin list view
    list_display = ('id', 'title', 'subject', 'author', 'rate', 'date_created', 'is_featured', 'is_active')
    
    # Fields with clickable links in the admin list view
    list_display_links = ('id', 'title')

    # Fields that are editable directly from the list view
    list_editable = ('is_featured', 'is_active')

    # Searchable fields
    search_fields = ('title', 'subject', 'author__user__username', 'rate')

    # Fields to filter results in the admin list view
    list_filter = ('is_featured', 'is_active', 'date_created', 'rate')

    # Add image uploads inline to TutorAd
    inlines = [AdsImagesAdmin]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    list_display_links = ('id', 'category_name')
    search_fields = ('category_name',)

class AdsImagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(TutorAd, AdsAdmin)
admin.site.register(AdsImages, AdsImagesAdmin)

admin.site.register(Author)

admin.site.register(Category)
