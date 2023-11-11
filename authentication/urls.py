from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name="validate-email"),
    path("activate/<uidb64>/<token>", views.VerificationView.as_view(), name="activate"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    
]