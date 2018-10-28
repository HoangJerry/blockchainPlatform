from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import BasePermission
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from . import api_utils
import requests
import pprint
import json
import ast

base_rpc_url = 'http://localhost:8080/'
rpc_headers = {'Content-Type': 'application/json'}
data = {"method": "personal_sign", "params":'',"id": 1}
gas = 1000000000000000000
from web3 import Web3
web3 = Web3(Web3.HTTPProvider("http://localhost:8080/"))



class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated 

class IsDoctor(BasePermission):
    message = 'You are not a doctor'
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role==UserBase.CONST_ROLE_DOCTOR


class UserCreate(generics.CreateAPIView):
    queryset = UserBase
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = web3.personal.newAccount(serializer.validated_data['password'])
        serializer.validated_data['block_chain_id'] = account
        serializer.validated_data['username'] = account
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request, format=None):
        block_chain_id = request.data.get('block_chain_id',None)
        password = request.data.get('password',None)
        message = request.data.get('message',None)
        print (request.user)
        if request.user.is_authenticated():
            user = request.user
        elif block_chain_id and password:
            data['method']="personal_sign"
            data['params']=[block_chain_id,block_chain_id,password]
            if message:
                data['params']=['0x'+message.encode("utf-8").hex(),block_chain_id,password]
            
            res = requests.post(base_rpc_url,data=json.dumps(data), headers=rpc_headers)
            # res= vars(res)
            ret = json.loads(res._content)
            if 'error' in ret:
                raise api_utils.BadRequest("Invalid account or password is wrong")

            user = UserBase.objects.get(username=block_chain_id)
        else:
            raise api_utils.BadRequest("Blockchain id or password is missing")
        if user:
            serializer = UserWithTokenSerializer(instance=user)
            return Response(serializer.data,status=HTTP_200_OK)
        raise api_utils.BadRequest("Invalid account or password is wrong")

class getBalance(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        if not request.user.username:
            raise api_utils.BadRequest("Invalid account")
        try:
            account = web3.eth.getBalance(Web3.toChecksumAddress(request.user.username))
            account = account/gas
        except Exception as e:
            raise api_utils.BadRequest(ast.literal_eval(str(e))[0])
        return Response({'my_balance':account},status=HTTP_200_OK)

class UserTestHistory(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTestHistorySerializer

    def get_queryset(self):
        is_rating = self.request.GET.get('is_rating',None)
        if is_rating:
            return self.request.user.patient_test_history.filter(status=TestHistory.CONST_STATUS_RATING).order_by('-creation_date');
        status = self.request.GET.get('status',None)
        if status:
            return self.request.user.patient_test_history.filter(status=status)
        return self.request.user.patient_test_history.all().order_by('-creation_date')

class DoctorTestHistory(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = UserTestHistorySerializer

    def get_queryset(self):
        return self.request.user.doctor_test_history.all()

class CreateTestHistory(generics.CreateAPIView):
    permission_classes = [IsDoctor]
    serializer_class = CreateTestHistorySerializer

    def create(self, request, *args, **kwargs):
        address = request.data.get('user',None)
        user = UserBase.objects.filter(username=address)
        if not user:
            raise api_utils.BadRequest("Invalid patient address")
      
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not int(request.data.get('price')) > 0:
            raise api_utils.BadRequest("Invalid price is zero")
        serializer.validated_data['user']= user[0]
        serializer.validated_data['doctor']= request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
class UpdateTestHistory(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTestHistorySerializer
    queryset = TestHistory

    def get_serializer_class(self):
        if self.request.user.role==UserBase.CONST_ROLE_PATIENT:
            return UserRatingSerializer
        return DoctorUpdateResultSerializer

    def patch(self, request, *args, **kwargs):
        if self.request.user.role==UserBase.CONST_ROLE_PATIENT:
            if self.request.user != self.get_object().user:
                raise api_utils.BadRequest("You are not patient of this test")
        if self.request.user.role==UserBase.CONST_ROLE_DOCTOR:
            if self.request.user != self.get_object().doctor:
                raise api_utils.BadRequest("You are not doctor of this test")
        return self.partial_update(request, *args, **kwargs)

class UserInfor(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class DataNameOfTest(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, format=None):
        return Response(TestHistory.CONST_NAME,status=HTTP_200_OK)


