from django import forms
from .models import WorkshopProfile, ServiceType
from .models import WorkshopGallary, AboutWorker

DAYS_OF_WEEK = [
    ('monday', 'Dushanba'),
    ('tuesday', 'Seshanba'),
    ('wednesday', 'Chorshanba'),
    ('thursday', 'Payshanba'),
    ('friday', 'Juma'),
    ('saturday', 'Shanba'),
    ('sunday', 'Yakshanba'),
]


class WorkshopProfileForm(forms.ModelForm):
    work_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = WorkshopProfile
        exclude = ['user', 'slug']
        fields = ['img', 'company_name', 'address', 'landmark', 'phone1', 'phone2',
                  'description', 'services', 'open_time', 'close_time', 'is_24_hours', 'work_days', 'branch','location_url']
        # add required fields for all
        required = {
            'img': True,
            'company_name': True,
            'address': True,
            'landmark': True,
            'phone1': True,
            'phone2': True,  # phone2 is optional
            'description': False,  # description is optional
            'services': True,
            'open_time': True,
            'close_time': True,
            'is_24_hours': False,  # is_24_hours is optional
            'work_days': False,  # work_days is optional
            'branch': False,  # branch is optional
            'location_url': True,  # location_url is optional
        }
        widgets = {
            'img': forms.FileInput(attrs={'class': 'file'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Avtosoz'}),
            'address': forms.TextInput(attrs={'placeholder': 'Boburshox ko’chasi 23a uy'}),
            'landmark': forms.TextInput(attrs={'placeholder': 'Davlat arxivi yoni'}),
            'phone1': forms.TextInput(attrs={'placeholder': '998', 'id': 'phoneInput1', 'maxlength': '12', 'onkeyup': 'formatPhoneNumber1();'}),
            'phone2': forms.TextInput(attrs={'placeholder': '998', 'id': 'phoneInput2', 'maxlength': '12', 'onkeyup': 'formatPhoneNumber2();'}),
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'services': forms.SelectMultiple(attrs={'id': 'types'}),
            'open_time': forms.TimeInput(attrs={'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'type': 'time'}),
            'is_24_hours': forms.CheckboxInput(attrs={'id': '24'}),
            'branch': forms.SelectMultiple(attrs={'id': 'branch-select'}),
            'location_url': forms.URLInput(attrs={'placeholder': 'Google Maps URL'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            qs = WorkshopProfile.objects.filter(user=user)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            self.fields['branch'].queryset = qs
        else:
            self.fields['branch'].queryset = WorkshopProfile.objects.none() 




class GalleryForm(forms.ModelForm):
    class Meta:
        model = WorkshopGallary
        fields = ['image']


class AboutWorkerForm(forms.ModelForm):
    class Meta:
        model = AboutWorker
        fields = ['about']
        widgets = {
            'about': forms.Textarea(attrs={'placeholder': "O'z haqingizda yozing"})
        }
