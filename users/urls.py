from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', views.register, name='register'),
    path('email-verification/<str:uid64>/<str:token>/', views.email_verification, name='email_verification'),
    path('email-verification-sent/', views.email_verification_sent, name='email_verification_sent'),
    path('email-verification-success/', views.email_verification_success, name='email_verification_success'),
    path('email-verification-failed/', views.email_verification_failed, name='email_verification_failed'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password-reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password-reset-sent.html'), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password-reset-form.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password-reset-complete.html'), name='password_reset_complete'),
]
