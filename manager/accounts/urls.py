from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "accounts"

#маршрутизатор

urlpatterns = [
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('register_user', views.register_user, name="register_user"),
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('edit/description', views.edit_description, name='edit-description'),
    path('edit/education-and-experience', views.edit_education_and_experience, name='edit-education-and-experience'),
    path('profile/', views.show_profile, name='show_profile'),
    path('profile/<int:pk>', views.show_profile_by_pk, name='profile'),
    path('all_profiles/', views.all_profiles, name='all_profiles'),
    path('coworkers/', views.show_coworkers, name='coworkers'),
    path('coworkers/<int:pk>', views.add_coworkers, name='add-coworkers'),
    path('message-form/', MessageFormView.as_view(), name='message-form')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root = settings.MEDIA_ROOT)
    
"""path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),"""

"""path('password-change/', auth_views.PasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),"""

