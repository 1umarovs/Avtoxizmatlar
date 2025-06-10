from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate
from .models import WorkshopProfile
from django.views.decorators.http import require_GET
from .forms import WorkshopProfileForm
from .models import WorkshopProfile, WorkshopGallary, AboutWorker , WorkshopRating
from .forms import GalleryForm,  AboutWorkerForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.crypto import get_random_string


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_mechanic = request.POST.get('user_type') == 'mechanic'  # "Men ustaman" tanlanganda

        if password1 == password2:
            user = User.objects.create_user(
                username=phone,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            login(request, user)

            if is_mechanic:
                return redirect('Users:settings')  # xizmat ko'rsatuvchi
            else:
                return redirect('/')  # haydovchi
    return render(request, 'signup.html')



def generate_unique_slug(company_name, instance=None):
    base_slug = slugify(company_name)
    unique_slug = base_slug
    num = 1
    while WorkshopProfile.objects.filter(slug=unique_slug).exclude(pk=instance.pk if instance else None).exists():
        unique_slug = f"{base_slug}-{num}"
        num += 1
    return unique_slug

def settings_view(request, slug=None):
    if slug:
        profile = get_object_or_404(WorkshopProfile, slug=slug, user=request.user)
    else:
        profile = WorkshopProfile.objects.filter(user=request.user).first()
        if profile:
            return redirect('Users:settings', slug=profile.slug)
        profile = None

    if request.method == 'POST':
        form = WorkshopProfileForm(request.POST, request.FILES, user=request.user, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.work_days = ','.join(form.cleaned_data.get('work_days', []))

            if profile:
                if profile.company_name != form.cleaned_data['company_name']:
                    obj.slug = generate_unique_slug(form.cleaned_data['company_name'], instance=profile)
            else:
                obj.slug = generate_unique_slug(form.cleaned_data['company_name'])

            obj.save()
            form.save_m2m()
            return redirect('Users:profile', slug=obj.slug)
    else:
        initial = {}
        if profile and profile.work_days:
            initial['work_days'] = profile.work_days.split(',')
        form = WorkshopProfileForm(instance=profile, initial=initial, user=request.user)

    return render(request, 'settings.html', {'form': form})


def my_all_workshops(request):
    workshops = WorkshopProfile.objects.filter(user=request.user)
    reviews = WorkshopRating.objects.filter(workshop__user=request.user).order_by('-id')[:5]
    
    # Formani user bilan yaratish
    form = WorkshopProfileForm(user=request.user)
    
    if request.method == 'POST':
        form = WorkshopProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.work_days = ','.join(form.cleaned_data['work_days'])
            obj.slug = generate_unique_slug(form.cleaned_data['company_name'])
            obj.save()
            form.save_m2m()
            return redirect('Users:profiles')  
    
    context = {
        'workshops': workshops,
        'form': form,
        'reviews': reviews
    }
    return render(request, 'profiles.html', context)

# 🔐 LOGIN VIEW
def login_view(request):
    error = None
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            profile = WorkshopProfile.objects.filter(user=user).first()
            if profile:
                return redirect('Users:settings', slug=profile.slug)
            else:
                return redirect('Users:settings')  # yangi profil yaratish uchun
        else:
            error = "Telefon raqam yoki parol noto‘g‘ri."
    return render(request, 'login.html', {'error': error})




# 👤 PROFILE VIEW
@login_required
def profile_view(request, slug):
    workshop = get_object_or_404(WorkshopProfile, slug=slug, user=request.user)
    shop = WorkshopProfile.objects.filter(slug=slug)
    print(shop)
    gallery_form = GalleryForm()
    about_form = AboutWorkerForm()

    if request.method == "POST":
        if 'add_gallery' in request.POST:
            gallery_form = GalleryForm(request.POST, request.FILES)
            if gallery_form.is_valid():
                gallery = gallery_form.save(commit=False)
                gallery.workshop = workshop
                gallery.save()
                return redirect('Users:profile', slug=slug)

        elif 'add_about' in request.POST:
            about_form = AboutWorkerForm(request.POST)
            if about_form.is_valid():
                about = about_form.save(commit=False)
                about.workshop = workshop
                about.save()
                return redirect('Users:profile', slug=slug)

    gallery_images = WorkshopGallary.objects.filter(workshop=workshop)
    abouts = AboutWorker.objects.filter(workshop=workshop)
    reviews = WorkshopRating.objects.filter(workshop=workshop).order_by('-id')

    context = {
        'gallery_form': gallery_form,
        'about_form': about_form,
        'gallery_images': gallery_images,
        'abouts': abouts,
        'workshop': shop,
        'reviews': reviews
    }


    return render(request, 'profile-details.html', context)


@require_GET
@login_required
def delete_gallery(request, pk):
    image = get_object_or_404(WorkshopGallary, pk=pk, workshop__user=request.user)
    image.delete()
    return JsonResponse({'success': True})



def user_logout(request):
    logout(request)
    return redirect('Users:login')  # foydalanuvchini login sahifasiga yo‘naltiradi

def delete_workshop(request, slug):
    profile = get_object_or_404(WorkshopProfile, slug=slug, user=request.user)
    profile.delete()
    return redirect('Users:profiles')


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password-reset-confirm.html'
    success_url = reverse_lazy('Users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        print("Form is valid, redirecting to:", self.success_url)  # Konsolga yozib qo'yamiz
        return response
