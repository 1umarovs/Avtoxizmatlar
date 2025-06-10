from django.contrib import admin
from .models import WorkshopProfile, ServiceType , WorkshopGallary, AboutWorker , WorkshopRating , MainService
# Register your models here.

@admin.register(MainService)
class MainServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

@admin.register(WorkshopRating)
class WorkshopRatingAdmin(admin.ModelAdmin):
    list_display = ('workshop', 'username', 'rating', 'comment')
    search_fields = ('workshop__company_name', 'username')
    list_filter = ('workshop', 'rating')
    ordering = ('-workshop__user__date_joined',)
    list_per_page = 20
    date_hierarchy = 'workshop__user__date_joined'
@admin.register(WorkshopGallary)
class WorkshopGallaryAdmin(admin.ModelAdmin):
    list_display = ('workshop', 'image')
    search_fields = ('workshop__company_name',)
    list_filter = ('workshop',)
    ordering = ('-workshop__user__date_joined',)
    list_per_page = 20
    date_hierarchy = 'workshop__user__date_joined'




@admin.register(AboutWorker)
class AboutWorkerAdmin(admin.ModelAdmin):
    list_display = ('workshop', 'about')
    search_fields = ('workshop__company_name',)
    list_filter = ('workshop',)
    ordering = ('-workshop__user__date_joined',)
    list_per_page = 20
    date_hierarchy = 'workshop__user__date_joined'

@admin.register(WorkshopProfile)
class WorkshopProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'address', 'phone1', 'is_24_hours')
    search_fields = ('company_name', 'address', 'phone1')
    prepopulated_fields = {'slug': ('company_name',)}
    list_filter = ('is_24_hours',)
    ordering = ('-user__date_joined',)
    list_per_page = 20
    date_hierarchy = 'user__date_joined'

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_per_page = 20