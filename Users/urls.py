from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Users'


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('settings/', views.settings_view, name='settings'),  # yangi profil
    path('settings/<slug:slug>/', views.settings_view, name='settings'),  # tahrirlash
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<slug:slug>/', views.profile_view, name='profile'),
    path('profiles/', views.my_all_workshops, name='profiles'),
    path('delete-gallery/<int:pk>/', views.delete_gallery, name='delete_gallery'),
    path('delete-workshop/<slug:slug>/', views.delete_workshop, name='delete_workshop'),

    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='password-reset.html',
        subject_template_name='email/password_reset_subject.txt',
        email_template_name='email/password_reset_email.html',
        success_url= reverse_lazy('Users:password_reset_done'),
    ), name='password_reset'),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password-reset-done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]