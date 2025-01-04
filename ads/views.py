from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Count
# Model Forms.
from .forms import PostAdsForm, AdsImagesForm
from django.contrib.auth.forms import User
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.mail import send_mail


from django.db.models import Q 
# importing messages
from django.contrib import messages

from ads.models import Author
# Create your views here.

# Post ads view
@login_required(login_url='login')
def post_ads(request):
    if request.method == 'POST':
        form = PostAdsForm(request.POST, request.FILES,user=request.user)
        
        if form.is_valid():

            # Save form but do not commit immediately
            tutor_ad = form.save(commit=False)
            tutor_ad.author = request.user.author  # Set the author as the current user
            tutor_ad.save()  # Now save the tutor ad

            # Handle images if provided
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    AdsImages.objects.create(ads=tutor_ad, image=image)
            

            # Email notification to admin
            mail_subject = "New Tutor Ad Submitted"
            message = f"Dear Admin, a new tutor ad has been submitted by {request.user.email}."
            send_mail(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return redirect('ads-listing')  # Redirect to the ad listing page after submission

    else:
        form = PostAdsForm()
        images_form = AdsImagesForm()
    return render(request, 'ads/post-ads.html', {'form': form,'images_form': images_form})

# Ads listing view
def ads_listing(request):
    ads_listing = TutorAd.objects.all()
    category_listing = Category.objects.annotate(total_ads=Count('tutor_ads')).order_by('category_name')

    context = {
        'ads_listing' : ads_listing,
        'category_listing' : category_listing
    }

    return render(request, 'ads/ads-listing.html', context)

# Ads detail view
def ads_detail(request, pk):
    ads_detail = get_object_or_404(TutorAd, pk=pk)
    ads_photos = AdsImages.objects.filter(ads=ads_detail)

    context = {
        'ads_detail' : ads_detail,
        'ads_photos' : ads_photos,
    }

    return render(request, 'ads/ads-detail.html', context)

# Ads category archive view
def ads_category_archive(request, slug):
    category = get_object_or_404(Category, slug=slug)
    ads_by_category = TutorAd.objects.filter(category=category)

    context = {
        'category' : category,
        'ads_by_category' : ads_by_category
    }

    return render(request, 'ads/category-archive.html', context)



# Ads author archive view
def ads_author_archive(request, pk):
    author = get_object_or_404(Author, pk=pk)
    ads_by_author = TutorAd.objects.filter(author=author)

    context = {
        'author' : author,
        'ads_by_author' : ads_by_author
    }

    return render(request, 'ads/author-archive.html', context)

# Ads search/filter view
def ads_search(request):

    keyword = request.GET.get('keyword', '')  # Retrieve the keyword from the search input
    category_name = request.GET.get('category_name')  # Retrieve the category if selected

    # Start with all ads and filter based on keyword and category
    ads_search_result = TutorAd.objects.all()

    # If keyword is present, filter ads based on the keyword matching title, subject, about_lesson, or about_tutor
    if keyword:
        ads_search_result = ads_search_result.filter(
            Q(title__icontains=keyword) |
            Q(subject__icontains=keyword) |
            Q(about_lesson__icontains=keyword) |
            Q(about_tutor__icontains=keyword)
        )

    # If category is selected, filter ads based on category
    if category_name:
        ads_search_result = ads_search_result.filter(category__category_name=category_name)

    context = {
        'ads_search_result': ads_search_result,
        'keyword': keyword,
        'category_name': category_name,
    }


    return render(request, 'ads/ads-search.html', context)

# Ads delete view
@login_required(login_url='login')
def ads_delete(request, pk):
    ad = get_object_or_404(TutorAd, pk=pk)
    ad.delete()
    return redirect("dashboard")

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(TutorAd, pk=pk, author=request.user.author)
    if request.method == 'POST':
        form = PostAdsForm(request.POST, instance=ad,user =request.user)
        images_form = AdsImagesForm(request.POST, request.FILES)
        if form.is_valid() and images_form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user.author
            ad.save()
            
            # Handle images if provided
            images = images_form.cleaned_data.get('images')
            for image in images:
                AdsImages.objects.create(ads=ad, image=image)
            
            return redirect('ads-detail', pk=ad.pk)
    else:
        form = PostAdsForm(instance=ad)
        images_form = AdsImagesForm()
    
    return render(request, 'ads/ads-update.html', {'form': form, 'images_form': images_form, 'ad': ad})







