"""
import django functions
"""
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password,check_password

"""
import apps,models,serializers
"""
from apps.account import models
from apps .account import serializers as rfid_serializers
from rfid_pro import settings
# from apps.admin import models as admin_models


"""
import restframeworks functions
"""
from rest_framework.views import APIView
from rest_framework import permissions,generics
from rest_framework import status

"""
import utils functions
"""
from utils import json,validators
from utils import functions
from utils import permissions as cust_perms

"""
other imports
"""
import json as j
import logging
import random as randint
from decouple import config
# from appsacmec_admin import models as admin_models
logger = logging.getLogger(__name__)
User = get_user_model()


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



def generate_random_password():
    # Define possible characters for PWD
    digits = "ABCDEFG@#$%^&*()!HIJKLMNOP1234567890"
    # Initialize PWD variable
    pwd = ""
    # Loop to generate 12 random digits
    for i in range(12):
        pwd += randint.choice(digits)
    # Return the PWD
    return pwd



class UserRegister(APIView):
    """
    Registeration of user
    """

    permission_classes=[permissions.AllowAny,cust_perms.ISSuperAdmin]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserRegister, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request):
        print("data_in")
        datas = j.loads(request.body.decode('utf-8'))
        print(datas)
        try:

                """
                User Email registeration
                """
                if validators.admin_email_register_validators(datas)==False:
                    return json.Response({"data":[]},"Required field is missing",400,False)

                if datas["firstname"]=="" or datas["lastname"]=="" or datas["phone_number"]=="" or datas["email"]=="" or datas["rfid_rssi_valu"]=="" or datas["ward_number"]=="" or datas["hospital_number"]=="" or datas["bed_number"]=="":
                    return json.Response({"data":[]},"Field is empty",400,False)
                
                Users_data = models.User.objects
                User_rfid = Users_data.filter(rfid_rssi_valu = datas["rfid_rssi_valu"])
                User_filter = Users_data.filter(phone_number=datas['phone_number'])
                User_email = Users_data.filter(email=datas['email'])

                if User_rfid.exists():
                    return json.Response({"data":[]},"Pfid value already exists!",400,False)

                if User_filter.exists():
                    return json.Response({"data":[]},"Phone number already exists!",400,False)
                
                if  User_email.exists():
                    return json.Response({"data":[]},"Email already exists!",400,False)
                
                # if datas["password"].lower() != datas["confirm_password"].lower():
                #     return json.Response({"data":[]}, "Password and confirm password are not same", 400, False)

                # if not models.role_master.objects.filter(id=datas['role']).exists():
                #     return json.Response({"data":[]},"There is no role for this type",400,False)

                rolelist = models.role_master.objects.filter(id=3).first()
    
                if str(rolelist).lower() == "patient":

                    Users_data.create(firstname=datas["firstname"],lastname=datas["lastname"],phone_number=datas['phone_number'],email=datas['email'],roles_id=rolelist.id,
                                      bed_number=datas['bed_number'], hospital_number=datas['hospital_number'],rfid_rssi_valu=datas['rfid_rssi_valu'],ward_number=datas['ward_number'])
                    user_datas = models.User.objects.get(email=datas['email'])
                    user_Name_id = models.User.objects.filter(email=datas['email']).first()
                    user_details = {}
                    getjwt=functions.emailauth(user_datas,user_Name_id.id)
                    # user_details['access_token'] = getjwt['access_token']
                    # user_details['refresh_token'] = getjwt['refresh_token']
                    user_details['user_info'] = {"id":user_Name_id.id,
                                                "name":str(user_Name_id.firstname) + str(user_Name_id.lastname),
                                                "email":user_Name_id.email,
                                                "phone_number":user_Name_id.phone_number}
                    return json.Response({"data":user_details},"User created successfully",201,True)
                
                else:
                    return json.Response({"data":[]},"Only user can be created",400,False)
                
        except Exception as e:
            return json.Response({"data":[]},f"{e}Internal Server Error", 400,False)
        

class loginApi(APIView):
    """
    login using Email
    """
    
    permission_classes=[permissions.AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(loginApi, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self,request):
        try:
            datas = j.loads(request.body.decode('utf-8'))
            if validators.Email_Login_Validators(datas) == False:
                print("email_false")
                return json.Response({"data":[]},"Required field is missing",400,False)
            
            user_data = models.User.objects

            if not user_data.filter(email=datas['email']).exists():
                print("exist")
                return json.Response({"data":[]},"Please enter registered email",400, False)

            if len(datas['password']) == 0 or datas['password'] == '':
                return json.Response({"data":[]},"Please enter password",400, False)
            
            users = user_data.get(email=datas['email'])

            if check_password(datas['password'],users.password) == False:
                print("check_password")
                return json.Response({"data":[]},"Incorrect password",400, False)

            user_datas = models.User.objects.get(email=datas['email'])
            user_Name_id = models.User.objects.filter(email=datas['email']).first()

            user_details = {}

            getjwt=functions.emailauth(user_datas,user_Name_id.id)
            user_details['access_token'] = getjwt['access_token']
            user_details['refresh_token'] = getjwt['refresh_token']
            user_details['user_info'] = {"id":user_Name_id.id,
                                                "name":str(user_Name_id.firstname)+' '+str(user_Name_id.lastname),
                                                "email":user_Name_id.email,
                                                "phone_number":user_Name_id.phone_number,
                                                "role_id":user_Name_id.roles_id}
            return json.Response({"data":user_details},"Logged In Successfully",200,True)

        except Exception as e:
            return json.Response({"data":[]},f"{e}Internal Server Error", 400,False)
        


class ChangePassword(APIView):
    """
    Change password once given forgot password
    """

    permission_classes=[permissions.AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ChangePassword, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self,request):
        
        try:
            datas = j.loads(request.body.decode('utf-8'))
            params = self.request.query_params
            if validators.change_password_validators(datas) == False:
                return json.Response({"data":[]},"Required field is missing",400,False)
            
            if datas["password"] == "" or datas["confirm_password"]=="" or datas["email"]=="":
                return json.Response({"data":[]},"Field is empty",400,False)
            


            Users_data = models.User.objects
            User_filter = Users_data.filter(id=params.get('id'),email=datas['email'])
            
            if not User_filter.exists():
                return json.Response({"data":[]},"Please enter valid email and valid id",400, False)
            
            if len(datas['password']) < 8 or datas['password'] == '':
                return json.Response({"data":[]},"Please enter password or length of password in short",400, False)
            

            if datas["password"].lower() != datas["confirm_password"].lower():
                return json.Response({"data":[]}, "Password and confirm password are not same", 400, False)
            
            if Users_data.get(email=datas['email']).is_email_verified == False:
                User_filter.update(password=make_password(datas["password"]),is_email_verified=True)
                return json.Response({"data":[]},"Password changed successfully",200, True)

            User_filter.update(password=make_password(datas["password"]))
            return json.Response({"data":[]},"Password changed successfully",200, True)
        except Exception as e:
            return json.Response({"data":[]},"Internal Server Error", 400,False)


# class ScanRfid(APIView):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(ScanRfid, self).dispatch(request, *args, **kwargs)

#     @csrf_exempt
#     def post(self,request):
#         try:
#             datas = j.loads(request.body.decode('utf-8'))
            
#             Users_data = models.User.objects

#             if Users_data.get(rfid_rssi_valu = datas['rfid_rssi_valu']):
#                 user_email= models.User.objects.filter(rfid_rssi_valu=datas['rfid_rssi_valu']).first()
#                 user_Name_id_ = user_email.out_perms
#                 email_body = (f"Alert msg for patient tag has no permissions{user_Name_id_}")
#                 email_subject="Alert MSG"
#                 mail=functions.send_mail_toTemplate(email_subject,email_body,user_email,settings.EMAIL_HOST_USER)  
                
#                 return json.Response({"data":[]},"Alert msg for patient ",200, True)
                
            
#             else:
#                 return json.Response({"data":[]},"rfid_rssi_value not exist",200, True)
#         except Exception as e:
#             return json.Response({"data":[e]},"Internal Server Error", 400,False)



class ScanRfid(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ScanRfid, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self,request):
        try:
            datas = j.loads(request.body.decode('utf-8'))

            queryset = models.rfid_db_table.objects.all()
            serializer_class = rfid_serializers.rifd_table_suggester
            
            Users_data = models.User.objects
            # rfid_table = models.rfid_db_table.objects

            if not Users_data.filter(rfid_rssi_valu = datas['rfid_value']):
                return json.Response({"data":[]},"No rfid value ",200, True)


            if Users_data.filter(rfid_rssi_valu = datas['rfid_value']):
                Users_data_=models.User.objects.filter(rfid_rssi_valu=datas['rfid_value']).first()
                
                # user_email=Users_data_.email
                user_email = config("ADMIN_EMAIL")
               

                rfid_table = models.rfid_db_table.objects
                


                if not (rfid_table.filter(rfid_value=datas['rfid_value'])).exists():
                    rfid_table.create(user_id=Users_data_.id, rfid_value = datas['rfid_value'])
                    user_gate_crossed = len(rfid_table.filter(rfid_value=datas['rfid_value']))
                    email_body = (f"Alert msg for patient tag has no permissions, and the User id is = {Users_data_.id} , and this many time he get out = {user_gate_crossed}")
                    email_subject="Alert MSG"
                    mail=functions.send_mail_toTemplate(email_subject,email_body,user_email,settings.EMAIL_HOST_USER)
                    return json.Response({"data":[]},"Alert msg for patient and rfid value first time scanned ",200, True)
                else:
                    rfid_table.create(user_id=Users_data_.id, rfid_value = datas['rfid_value'])
                    user_gate_crossed = len(rfid_table.filter(rfid_value=datas['rfid_value']))
                    email_body = (f"Alert msg for patient tag has no permissions, and the User id is = {Users_data_.id} , and this many time he get out = {user_gate_crossed}")
                    email_subject="Alert MSG"
                    mail=functions.send_mail_toTemplate(email_subject,email_body,user_email,settings.EMAIL_HOST_USER)  
                
                    return json.Response({"data":[]},"Alert msg for patient and rfid value already exists ",200, False)
                
            
            else:
                return json.Response({"data":[]},"rfid_rssi_value not exist",200, True)
        except Exception as e:
            return json.Response({"data":[e]},"Internal Server Error", 400,False)



class rfid_suggester(generics.GenericAPIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(rfid_suggester, self).dispatch(request, *args, **kwargs)
    
    queryset = models.rfid_db_table.objects.all()
    serializer_class = rfid_serializers.rifd_table_suggester

    
    def get(self, request):
        try:
            # print("fdklfj")
            
            # serializer_=models.rfid_db_table.objects.all()
            # print(serializer_)
            queryset = self.filter_queryset(self.get_queryset())            
            serializer = self.get_serializer(queryset, many=True)
            data = json.Response(serializer.data,'Listed successfully',200,True)
            return data 
        except Exception as e:
            return json.Response({'data':[]},f'{e}Internal Server Error',400,False)
        

        
        




# class ForgetAccount(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self,request):
#         try:
#             data=request.data
#             email=data['email']
#             check_email=User.objects.filter(email=email).exists()
#             if not check_email:
#                 # res = {"status":False,'message':'Kindly Enter The Registered email','data':[]}
#                 return json.Response({'data':[]},f'{e}Internal Server Error',400,False)
            
#             user=models.User.objects.filter(email=email).last()
#             # generate OTP and save with USERTEMP
#             otp_val=generate_otp()
#             # otp_val = 1234
#             email_body = (f"Use This Otp for verification {otp_val}")
#             email_subject="forget_password"
#             mail=functions.send_mail_toTemplate(email_subject,email_body,email,settings.EMAIL_HOST_USER)  
            
#             save_temp=models.OTPAuth.objects.create(otp=otp_val,user_id=user.id)
            
#             return json.Response({"data":[]},"OTP send successfully to given email",200, True)
                       
#         except Exception as e:
#             logger.info(f"{e}: forget password")
#             return json.Response({"data":[]},f"{e}Internal Server Error", 400,False)


class forget_password(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        try:
            data=request.data
            email=data['email']
            check_email=User.objects.filter(email=email).exists()
            if not check_email:
                # res = {"status":False,'message':'Kindly Enter The Registered email','data':[]}
                return json.Response({'data':[]},f'{e}Internal Server Error',400,False)
            # data = request.data
            Users_data = models.User.objects
            user=models.User.objects.filter(email=email).last()
            # generate OTP and save with USERTEMP
            # otp_val=generate_otp()
            original_password_ = generate_random_password()
            print(original_password_)
            password_ = make_password(original_password_)
            
            # print(otp_val)
            # otp_val=123555
            email_body = (f"Use This Otp for verification {original_password_}")
            email_subject="forget_password"


            mail=functions.send_mail_toTemplate(email_subject,email_body,data['email'],settings.EMAIL_HOST_USER)  
            
            # save_temp=models.OTPAuth.objects.update(otp=otp_val,user_id=user.id)
            if Users_data.get(email=data['email']):
                Users_data.update(password=password_)

            Users_data.update(password=password_)
            
            return json.Response({"data":[]},"OTP send successfully to given email",200, True)
                       
        except Exception as e:
            logger.info(f"{e}: forget password")
            return json.Response({"data":[]},f"{e}Internal Server Error", 400,False)
