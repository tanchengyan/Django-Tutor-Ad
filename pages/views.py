from django.shortcuts import render, get_object_or_404

from ads.models import*
from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings

from urllib.parse import urlparse, urlunparse
# Model Forms.

# Create your views here.

# Home view
def home(request):
    
    # Fetch recent tutor ads
    recent_ads = TutorAd.objects.filter(is_active=True).order_by('-date_created')[:3]
    
    # Fetch featured tutor ads
    featured_ads = TutorAd.objects.filter(is_featured=True, is_active=True)
    
    # Browse tutor ads by Category
    category_listing = Category.objects.all()

    # Fetch search category 
    category_search = Category.objects.values_list('category_name', flat=True).distinct().order_by("category_name")
    
    # Contexts
    context = {
        'recent_ads': recent_ads,
        'featured_ads': featured_ads,
        'category_search': category_search,
        'category_listing': category_listing,
    }

    return render(request, 'pages/index.html', context)

# Faq view
def faq(request):
    return render(request, 'pages/faq.html')

# Terms of service view
def terms_of_service(request):
    return render(request, 'pages/terms-of-service.html')

# Contact view
def contact(request):
    return render(request, 'pages/contact.html')

# def switch_language(request):
#     lang_code = request.GET.get('language', 'en')
#     translation.activate(lang_code)
#     response = redirect(request.META.get('HTTP_REFERER', '/'))
#     response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
#     return response

def switch_language(request):
    lang_code = request.GET.get('language', 'en')
    translation.activate(lang_code)
    
    # Get the referrer URL
    referrer = request.META.get('HTTP_REFERER', '/')
    
    # Parse the URL
    parsed_url = urlparse(referrer)
    
    # Remove the language prefix from the path
    path = parsed_url.path
    for lang in dict(settings.LANGUAGES).keys():
        if path.startswith(f'/{lang}/'):
            path = path[len(f'/{lang}'):]
            break
    
    # Reconstruct the URL without the language prefix
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    
    # Redirect to the modified URL
    response = redirect(new_url)
    
    # Set the language cookie
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    
    return response