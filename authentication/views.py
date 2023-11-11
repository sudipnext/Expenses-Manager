from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
#for user email authentication
from django.core.mail import EmailMessage
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from userpreferences.models import UserPreference




# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry the email is already in use please choose another one'}, status=409)
        return JsonResponse({'email_valid': True})   

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username_should_only_contain_alphanumeric_characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry! username is already in Use'}, status=409)
        return JsonResponse({'username_valid':True})
    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        # messages.success(request, "Successs")
        # messages.error(request, "Error")
        # messages.warning(request, "Warning")
        # messages.info(request, 'Information')
        username = request.POST["username"]
        email = request.POST["email"]
        password= request.POST["password"]

        context={
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password is Short")
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active= False
                user.save()

                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate',kwargs={'uidb64': uidb64,'token': token_generator.make_token(user) })
                activate_url="http://"+domain+link
                email_subject="Activate Your Account"
                email_body= "Namaste "+user.username+" Please use this link to verify this account\n"+ activate_url
                email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@expenses.com',
                        [email],
                )
                email.send(fail_silently=False)
                messages.success(request, "Account has been Created")
                return render(request, 'authentication/register.html')

                    
        return render(request, 'authentication/register.html')
    
#we need a class for verification
# use use unique tokens which can be used
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already Activated')
            
            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            messages.success(request, 'Account activated successfully!')
            return redirect('login')

        except Exception as ex:
            pass
        return redirect('login')
            
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)

                    # Check if UserPreference exists for the user
                    if not UserPreference.objects.filter(user=user).exists():
                        UserPreference.objects.create(user=user)

                    messages.success(request, 'Welcome, '+user.username+' You are now logged in')
                    return redirect('expenses')
                else:
                    messages.error(request, 'Account is not active, please check your email')        
                    return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid Credentials, Try Again')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Please fill all the fields')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been Logged Out")
        return redirect('login')

