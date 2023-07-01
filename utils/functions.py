from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import re
from django.core.mail import EmailMessage

from random import randint

# import qrcode
from base64 import b64encode


def emailauth(user,id):
    access = AccessToken.for_user(user)
    refresh=RefreshToken.for_user(user)

    access['email']=user.email
    access['user_id']=id
    refresh['email']=user.email
    refresh['user_id']=id
    
    return {"access_token": str(access),
    "refresh_token":str(refresh)}


def send_mail_toTemplate(subject,mail_body,to_mail,from_mail):
    try:
        email = EmailMessage(
            subject=subject,body=mail_body,to=[to_mail],from_email=from_mail
        )
        email.send()
        return True
    except Exception as ex:
        raise ex
    

def generate_otp():
    # Define possible characters for OTP
    digits = "123456789"
    # Initialize OTP variable
    otp = ""
    # Loop to generate 6 random digits
    for i in range(4):
        otp += randint.choice(digits)
    # Return the OTP
    return otp
        