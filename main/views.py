from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render , get_object_or_404, redirect
from django.http import JsonResponse
from Users.models import WorkshopProfile, ServiceType , WorkshopRating , AboutWorker , WorkshopGallary , MainService
from django.db.models import Q


def categories(request):

    workshops = WorkshopProfile.objects.all()
    main_categories = MainService.objects.prefetch_related('service_types').all()
    reviews = WorkshopRating.objects.all().order_by('-id')[:5]

    # Pagination
    paginator = Paginator(workshops, 3)  # 3 workshops per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'workshops': page_obj,
        'reviews': reviews,
        'main_categories': main_categories
    }

    return render(request, 'category.html', context)

def filter_categories(request, slug):
    service_type = ServiceType.objects.filter(slug=slug).first()
    main_categories = MainService.objects.prefetch_related('service_types').all()


    workshops = WorkshopProfile.objects.filter(services=service_type)
    reviews = WorkshopRating.objects.filter(workshop__services=service_type).order_by('-id')[:5]

    # Pagination
    paginator = Paginator(workshops, 6)  # 6 workshops per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'category': service_type,
        'workshops': page_obj,
        'reviews': reviews,
        'main_categories': main_categories
    }

    return render(request, 'category.html', context)

def home(request):
    service_types = MainService.objects.all()
    service = ServiceType.objects.all().order_by('?')[:6]  # Tasodifiy 6 ta xizmat turini olish
    return render(request, 'index.html', {'service_types': service_types, 'services': service})

def get_subcategories_by_slug(request, main_slug):
    print(f"✅ AJAX so‘rovi qabul qilindi: slug = {main_slug}")  # Bu terminalda chiqadi

    try:
        main_service = MainService.objects.get(slug=main_slug)
        subcategories = main_service.service_types.all()
        data = [{'name': sub.name, 'slug': sub.slug} for sub in subcategories]
        return JsonResponse({'subcategories': data})
    except MainService.DoesNotExist:
        print("❌ Xatolik: Bunday slug topilmadi!")
        return JsonResponse({'subcategories': []})


def search_workshops(request):
    main_categories = MainService.objects.prefetch_related('service_types').all()
    query = request.GET.get('search', '')
    if query and len(query) >= 3 and request.method == 'GET':
        workshops = WorkshopProfile.objects.filter(
            Q(company_name__icontains=query) | 
            Q(services__name__icontains=query)
        ).distinct()
        reviews = WorkshopRating.objects.filter(workshop__in=workshops).order_by('-id')[:5]
    else:
        workshops = WorkshopProfile.objects.none()
        reviews = WorkshopRating.objects.filter(workshop__in=workshops).order_by('-id')[:5]

    # Pagination
    paginator = Paginator(workshops, 6)  # 6 workshops per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'workshops': page_obj,
        'reviews': reviews,
        'query': query,
        'main_categories': main_categories
    }

    return render(request, 'category.html', context)

def workshop_details(request, slug):
    workshop = get_object_or_404(WorkshopProfile, slug=slug)
    reviews = WorkshopRating.objects.filter(workshop=workshop).order_by('-id')

    if request.method == 'POST':
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        print(name, review, rating)

        if name and review and rating:
            WorkshopRating.objects.create(
                workshop=workshop,
                username=name,
                comment=review,
                rating=int(rating)
            )
            # Shu joyni o‘zgartirdik: foydalanuvchini hozirgi sahifaga qaytaramiz
            return redirect(request.META.get('HTTP_REFERER', '/'))

    gallery_images = WorkshopGallary.objects.filter(workshop=workshop)
    abouts = AboutWorker.objects.filter(workshop=workshop)

    context = {
        'workshop': workshop,
        'gallery_images': gallery_images if gallery_images.exists() else None,
        'abouts': abouts,
        'reviews': reviews,

    }

    return render(request, 'category-detail.html', context)