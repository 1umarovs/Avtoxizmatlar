from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify

class WorkshopProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshops')
    img = models.ImageField(upload_to='profile_images/',  blank=True)  # Profil rasmi
    company_name = models.CharField(max_length=255)  # Xizmat shirkat nomi
    slug = models.SlugField(max_length=255, unique=True)  # Xizmat shirkat nomi (slug)
    address = models.CharField(max_length=255)       # Manzil
    landmark = models.CharField(max_length=255)      # Mo’ljal
    phone1 = models.CharField(max_length=20)         # Telefon 1
    phone2 = models.CharField(max_length=20, blank=True, null=True)  # Telefon 2
    description = models.TextField()                 # Xizmatlar haqida
    services = models.ManyToManyField('ServiceType') # Xizmat turlari
    open_time = models.TimeField()                   # Ish boshlanishi
    close_time = models.TimeField()                  # Ish tugashi
    is_24_hours = models.BooleanField(default=False) # 24 soatmi
    work_days = models.CharField(max_length=100)     # Ish kunlari (json ko‘rinishda saqlansa bo'ladi)
    branch = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='branches')  # Filiallar
    location_url = models.URLField(blank=True, null=True)  # Joylashuv URLsi


    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = 'Workshop Profile'
        verbose_name_plural = 'Workshop Profiles'
        ordering = ['company_name']

    def avg_rating(self):
        ratings = WorkshopRating.objects.filter(workshop=self)
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(),2)
        return 0



    def save(self, *args, **kwargs):
        if not self.slug or self._state.adding or self._company_name_changed():
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.company_name)
        unique_slug = base_slug
        num = 1
        while WorkshopProfile.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        return unique_slug

    def _company_name_changed(self):
        if not self.pk:
            return True
        old = WorkshopProfile.objects.filter(pk=self.pk).first()
        return old and old.company_name != self.company_name

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    maincategory = models.ForeignKey('MainService', on_delete=models.CASCADE, related_name='service_types',blank=True, null=True)  # Asosiy xizmat turi

    def __str__(self):
        return self.name

class MainService(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)  # Slug maydonini qo'shamiz
    icon = models.ImageField(upload_to='main_icons/', null=True, blank=True)  # tepadagi rasm

    def __str__(self):
        return self.name



class WorkshopGallary(models.Model):
    workshop = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE , related_name='gallary')
    image = models.ImageField(upload_to='workshop_gallery/')


    def __str__(self):
        return f"{self.workshop.company_name} - {self.image.url}"
    

class AboutWorker(models.Model):
    workshop = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    about = models.TextField()

    def __str__(self):
        return f"{self.workshop.company_name} - About"
    
class WorkshopRating(models.Model):
    workshop = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True, null=True)
    rating = models.IntegerField()
    comment = models.TextField()


    def avg_rating(self):
        ratings = WorkshopRating.objects.filter(workshop=self.workshop)
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0

    def __str__(self):
        return f"{self.workshop.company_name}  - {self.rating}"