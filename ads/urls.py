from django.urls import path,include

from .import views

urlpatterns = [
    path('post-ads/', views.post_ads, name='post-ads'),
    path('ads-listing/', views.ads_listing, name='ads-listing'),
    path('edit-ad/<int:pk>/', views.edit_ad, name='edit-ad'),
    path('ads/<int:pk>/', views.ads_detail, name='ads-detail'),
    path('ads/<int:pk>/delete/', views.ads_delete, name='ads-delete'),
    path('category/<slug:slug>/', views.ads_category_archive, name='category-archive'),

    path('author/<int:pk>/', views.ads_author_archive, name='author-archive'),
    path('ads-search/', views.ads_search, name='ads-search'),

    path('ckeditor5/', include('django_ckeditor_5.urls'))
]