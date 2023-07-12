from django.urls import path
from apps.account import views

app_name = 'account'

urlpatterns = [

    path('registeruser/',views.UserRegister.as_view(),name='registeruser'),
    path('email_login/',views.loginApi.as_view(),name='email_login'),
    path('changepassword/',views.ChangePassword.as_view(),name='changepassword'),
    path('scan/',views.ScanRfid.as_view(),name='scan'),
    path('rfid_suggest/',views.rfid_suggester.as_view(),name='rfid_suggester'),
    # path('forget_accnt/',views.ForgetAccount.as_view(),name='forget_accnt'),
    path('forget_password/',views.forget_password.as_view(),name='forget_password'),
    # path('role_view/',views.roles_master.as_view(),name='roleview'),

]