from django.urls import path
from .views import UserSignUp, PasswordEditView, login_user, logout_user, ResetPasswordView, ActivateAccount #, PasswordResetConfirmView, PasswordResetCompleteView
from .views import ShowProfile, EditProfilePage, CreateProfilePage, EditProfile, DraftProfile

from django.contrib.auth import views as auth_views
from . import views

#from .view import ContactView
urlpatterns = [

    path('register/',UserSignUp.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login_user/', views.login_user, name="login"),

    path('logout_user/', views.logout_user, name="logout"),

    path('password/',PasswordEditView.as_view(), name='password-change'),
    path('password_success/',views.password_success,name='password_success'),

    path('password_reset/',ResetPasswordView.as_view(),name='password_reset'),
    

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', post_reset_login= True),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    

    path('edit_profile/',EditProfile.as_view(), name='edit_profile'),
    path('<int:pk>/profile/',ShowProfile.as_view(), name='show_profile'),
    path('<int:pk>/profile/draft/',DraftProfile.as_view(), name='draft_profile'),

    path('<int:pk>/edit_profile_page/',EditProfilePage.as_view(), name='edit_profile_page'),
    path('create_profile_page/',CreateProfilePage.as_view(), name='create_profile_page'),


]