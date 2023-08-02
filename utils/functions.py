from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import re
from django.core.mail import EmailMessage
import pytz
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
    
    
    
    #expiry time for verifing otp
def verifyexpiry_time(expirytime):
    utc = pytz.UTC
    curnt_time = datetime.now()
    dt_string = str(expirytime)
    new_dt = dt_string[:19]
    curnt_time = datetime.strptime(str(curnt_time), '%Y-%m-%d %H:%M:%S.%f')
    expire_ts = datetime.strptime(new_dt, '%Y-%m-%d %H:%M:%S.%f')
    month_name = expirytime.strftime("%d")+" "+expirytime.strftime("%b") +" "+expirytime.strftime("%Y")
    time = expirytime.strftime("%H")+":"+expirytime.strftime("%M")
    print('month name: ', month_name, "time: ",)
    curnt_time = curnt_time.replace(tzinfo=utc)
    expire_ts = expire_ts.replace(tzinfo=utc)
    return expire_ts,curnt_time


def send_mail_toTemplate(subject,mail_body,to_mail,from_mail):
    try:
        email = EmailMessage(
            subject=subject,body=mail_body,to=[to_mail],from_email=from_mail
        )
        email.send()
        return True
    except Exception as ex:
        raise ex
    

# def generate_otp():
#     # Define possible characters for OTP
#     digits = "123456789"
#     # Initialize OTP variable
#     otp = ""
#     # Loop to generate 6 random digits
#     for i in range(4):
#         otp += randint.choice(digits)
#     # Return the OTP
#     return otp
        