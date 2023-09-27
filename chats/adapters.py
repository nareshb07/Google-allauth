# from allauth.account.adapter import DefaultAccountAdapter
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from .models import User

# class CustomAccountAdapter(DefaultAccountAdapter):
#     def pre_social_login(self, request, sociallogin):
#         # Check if a user account already exists with the same email
#         email = sociallogin.account.extra_data['email']
#         user_model = User()
#         try:
#             user = user_model.objects.get(email=email)
#             # Associate the Google account with the existing user account
#             sociallogin.connect(request, user)
#         except user_model.DoesNotExist:
#             # No existing user account found, proceed with the regular flow
#             pass

# class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
#     def pre_social_login(self, request, sociallogin):
#         # Skip the email verification step for Google authentication
#         if sociallogin.account.provider == 'google':
#             sociallogin.user.email_verified = True

        
#     def is_auto_signup_allowed(self, request, sociallogin):
#         # Disable automatic signup for Google authentication
#         return False

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User  # Import the User model
from urllib.parse import urlparse, urlunparse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_safe_url(self, url):
        # Implement your URL validation logic here
        # For example, you can check if the URL starts with 'http://' or 'https://'
        parsed_url = urlparse(url)
        return parsed_url.scheme in ('http', 'https')
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        
        # Check if the user already has a username
        if not user.username:
            # Generate a unique username based on the user's email
            base_username = user.email.split('@')[0]    
            username = base_username
            count = 1

            # Ensure the username is unique
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{count}"
                count += 1

            user.username = username

        return user



    # def new_user(self, request, sociallogin):
    #     # Check if a user account already exists with the same email
    #     email = sociallogin.account.extra_data.get('email')
    #     if email:
    #         try:
    #             user = EmailAddress.objects.get(email=email).user
    #             # Associate the Google account with the existing user account
    #             sociallogin.connect(request, user)
    #             # Redirect to the login success page
    #             return redirect('account_login_success')
    #         except EmailAddress.DoesNotExist:
    #             pass



from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from chats.models import User
from allauth.socialaccount.helpers import perform_login 

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        
        if user.id:  
            return          
        try:
            customer = User.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'                
            perform_login(request, customer, 'none')
        except User.DoesNotExist:
            pass




####################################################################################



######################################################################################

