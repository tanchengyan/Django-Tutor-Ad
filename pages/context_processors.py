from ads.models import *

def footer_recent_ads(request):
    ads = TutorAd.objects.filter(is_active=True).order_by('-date_created')[0:2]
    return {
        'footer_recent_ads' : ads
    }
