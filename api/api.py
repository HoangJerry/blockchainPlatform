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
from solc import compile_source

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
        return request.user and request.user.is_authenticated and (request.user.role==UserBase.CONST_ROLE_DOCTOR or request.user.is_superuser==True)


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
    serializer_class   = UserTestHistorySerializer

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserBase.objects.filter(username=serializer.validated_data['user'])
        if not user:
            raise api_utils.BadRequest("Invalid patient address")
        if not int(request.data.get('price')) > 0:
            raise api_utils.BadRequest("Invalid price is zero")
        serializer.validated_data['user']= user[0]
        serializer.validated_data['doctor']= request.user
        web3.eth.defaultAccount = request.user.username
        print(request.data.get('password'))
        web3.personal.unlockAccount(request.user.username,request.data.get('password'))

        # Create then input address and abi
        self.perform_create(serializer)
        contract = web3.eth.contract(
            address= '0x7dF41bc443c1aBEb32340435127b6DA82cF4a5b3',
            abi='''[ { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "testHistoriesAccts", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x04f7f327" }, { "constant": true, "inputs": [], "name": "getBalance", "outputs": [ { "name": "", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x12065fe0" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "balances", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x27e235e3" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_result", "type": "string" } ], "name": "setResult", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x31027970" }, { "constant": false, "inputs": [], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function", "signature": "0x3ccfd60b" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_patient", "type": "address" }, { "name": "_price", "type": "uint256" } ], "name": "setTestHistory", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x62a5814e" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "getTestHistory", "outputs": [ { "name": "", "type": "address" }, { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0xad601c88" }, { "constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0xd0e30db0" } ]''',
        )

        tx_hash = contract.functions.setTestHistory(serializer.data['id'],user[0].username,serializer.data['price']).transact()
        # print(tx_hash)
        web3.eth.waitForTransactionReceipt(tx_hash)
        temp =contract.functions.getTestHistory(serializer.data['id']).call()
        print(temp)
        # pprint.pprint()
        web3.personal.lockAccount(request.user.username)
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        contract = web3.eth.contract(
            address= '0x7dF41bc443c1aBEb32340435127b6DA82cF4a5b3',
            abi='''[ { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "testHistoriesAccts", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x04f7f327" }, { "constant": true, "inputs": [], "name": "getBalance", "outputs": [ { "name": "", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x12065fe0" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "balances", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x27e235e3" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_result", "type": "string" } ], "name": "setResult", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x31027970" }, { "constant": false, "inputs": [], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function", "signature": "0x3ccfd60b" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_patient", "type": "address" }, { "name": "_price", "type": "uint256" } ], "name": "setTestHistory", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x62a5814e" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "getTestHistory", "outputs": [ { "name": "", "type": "address" }, { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0xad601c88" }, { "constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0xd0e30db0" } ]''',
        )
        if not instance.result==None:
            try:
                tx_hash = contract.function.setResult(instance.id, instance.result).transact()
                web3.eth.waitForTransactionReceipt(tx_hash)
            except Exception as e:
                raise e

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
class UserDeposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        web3.eth.defaultAccount = request.user.username
        web3.personal.unlockAccount(request.user.username,request.data.get('password'))
        contract = web3.eth.contract(
            address= '0x7dF41bc443c1aBEb32340435127b6DA82cF4a5b3',
            abi='''[ { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "testHistoriesAccts", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x04f7f327" }, { "constant": true, "inputs": [], "name": "getBalance", "outputs": [ { "name": "", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x12065fe0" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "balances", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x27e235e3" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_result", "type": "string" } ], "name": "setResult", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x31027970" }, { "constant": false, "inputs": [], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function", "signature": "0x3ccfd60b" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_patient", "type": "address" }, { "name": "_price", "type": "uint256" } ], "name": "setTestHistory", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x62a5814e" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "getTestHistory", "outputs": [ { "name": "", "type": "address" }, { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0xad601c88" }, { "constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0xd0e30db0" } ]''',
        )
        print( "coca")
        tx_hash = contract.functions.deposit().transact()
        print( "coca")
        web3.eth.waitForTransactionReceipt(tx_hash)
        web3.personal.lockAccount(request.user.username)
        return Response({'status':'done'},status=HTTP_200_OK)

class UserInfor(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = UserSerializer

    def get_object(self):
        return self.request.user

class DataNameOfTest(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, format=None):
        return Response(TestHistory.CONST_NAME,status=HTTP_200_OK)
        
        