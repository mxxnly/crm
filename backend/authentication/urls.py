from django.urls import path
from .views import login_view, logout_view, register_view, home_view, profile_view, verify_email_view, send_to_review
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('tasks/send-to-review/<int:task_id>/', send_to_review, name='send_to_review'),
     path('auth/login/', login_view, name="login"),
     path('auth/logout/', logout_view, name="logout"),
     path('auth/register/', register_view, name="register"),
     path('auth/verify/', verify_email_view, name='verify_email'),
     path('', home_view, name="home"),
     path('profile/', profile_view, name="profile"),
     path('password-reset/', 
           auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), 
           name='password_reset'),
     path('password-reset/done/', 
           auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), 
           name='password_reset_done'),
     path('reset/<uidb64>/<token>/', 
           auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), 
           name='password_reset_confirm'),
     path('reset/done/', 
           auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), 
           name='password_reset_complete'),
]
