from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='category_all'),  # Barchasi
    path('categories/<slug:slug>/', views.filter_categories, name='category'),  # Har bir kategoriya
    path('workshop/details/<slug:slug>/', views.workshop_details, name='workshop_detail'),
    path('workshop/', views.search_workshops, name='search_workshops'),
    path('get-subcategories/<slug:main_slug>/', views.get_subcategories_by_slug, name='get_subcategories_by_slug'),
    
]