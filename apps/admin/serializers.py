from django.contrib.auth import get_user_model
from rest_framework import serializers
# from apps.account.serializers import rifd_table_suggester
from apps.account.serializers import *
from apps.account.models import *

User = get_user_model()


class Rfid_TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = rfid_db_table
        fields = ['user_id','rfid_value','updated_at']



"""
Users Listing serializer
"""
class UserListSerializer(serializers.ModelSerializer):
    # roles = serializers.SerializerMethodField('get_roles')
    # role_id = serializers.SerializerMethodField('get_role_id')
    # rfid_table = Rfid_TableSerializer(many=True)
    rfid_table = Rfid_TableSerializer(many=True)

    

    # def get_roles(self,data):
    #     role = account_model.role_master.objects.get(id=data.roles_id)
    #     return str(role)

    # def get_role_id(self,data):
    #     role = data.roles_id
    #     return str(role)
    
    class Meta:
        model = User

        fields = ['id','firstname','lastname','email','phone_number','ward_number','hospital_number','bed_number','out_perms','rfid_table']



class UserDetailViewSerializers(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField('get_roles')
    role_id = serializers.SerializerMethodField('get_role_id')

    def get_roles(self,data):
        role = account_model.role_master.objects.get(id=data.roles_id)
        return str(role)

    def get_role_id(self,data):
        role = data.roles_id
        return role

    class Meta:
        model = User
        fields = ['id','firstname','lastname','email','phone_number','roles','role_id','ward_number','hospital_number','bed_number','out_perms']



