# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from turtle import Turtle
# from types import CoroutineType

from django.contrib.auth import models as auth_models
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from apps.account import managers

from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

# from apps.generics import models as generic_models
# from apps.generics import tasks



class User(auth_models.AbstractBaseUser):
    """Custom user model that supports using email instead of username"""

    firstname = models.CharField(max_length=64)

    lastname = models.CharField(max_length=64)

    email = models.EmailField(max_length=64, unique=True)

    bed_number = models.TextField(blank=True, null=True)

    hospital_number  = models.CharField(max_length=50,null=True,validators=[alphanumeric])

    rfid_rssi_valu = models.TextField(blank=True, null=True,validators=[alphanumeric])

    ward_number = models.TextField(blank=True, null=True)

    phone_number = models.CharField(max_length=100, blank=True, null=True)

    roles = models.ForeignKey('role_master', blank=True, null=True, on_delete=models.CASCADE)

    out_perms = models.BooleanField(default=False)

    


    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    @property
    def get_roles(self):
        if self.roles:
            return self.roles.name

    @property
    def is_admin(self):
        return self.get_roles and self.get_roles in ['SuperAdmin','Admin','patient']
    
    def has_perm(self, perm, obj=None):
       return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin


    @classmethod
    def create_user(cls, email):
        if email and not User.objects.filter(email=email).exists():
            role, _ = role_master.objects.get_or_create(name='User')
            User.objects.create_user(email=email, roles=role)


class OTPAuth(models.Model):
    "Model for handling user authentication via OTP"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=12)
    expired_by = models.DateTimeField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        db_table = 'rfid_otp_auth'



class role_master(models.Model):
    "Model for handling user role"
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Role master')
        verbose_name_plural = _('Role masters')



class rfid_db_table(models.Model):
    rfid_value = models.TextField(blank=True, null=True,validators=[alphanumeric])

    created_at = models.DateTimeField(auto_now= True,null=True)

    updated_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return str(self.rfid_value)
# class MangeUserLog(generic_models.UUIDModel):
#     """
#     Models for handling users page log time and which page logged"""

#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     types = models.CharField(max_length= 200,null=True)
#     descriptions = models.TextField(null=True)
#     created_on = models.DateTimeField(auto_now=True,null=True)

#     class Meta:
#         verbose_name = _('Manage User Log')
#         verbose_name_plural = _('Manage User Logs')



