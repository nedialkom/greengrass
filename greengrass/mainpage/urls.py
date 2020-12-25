from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        subject_template_name='password_reset_subject.txt',
        email_template_name='password_reset_email.html',
        ),
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
        ),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'),
    path('auto_on/', views.auto_on, name='auto_on'),
    path('auto_off/', views.auto_off, name='auto_off'),
    path('set_target_humidity/', views.set_target_humidity, name='set_target_humidity'),
    path('irrigation_on/', views.irrigation_on, name='irrigation_on'),
    path('irrigation_off/', views.irrigation_off, name='irrigation_off'),
    path('about/', views.about, name='about'),
]
