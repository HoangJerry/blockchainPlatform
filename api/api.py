from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
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

from web3 import Web3
web3 = Web3(Web3.HTTPProvider("http://localhost:8080/"))


class AccountsList(APIView):
    pass

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

    def post(self, request, format=None):
        block_chain_id = request.data.get('block_chain_id',None)
        if not block_chain_id:
            raise api_utils.BadRequest("Invalid account")
        try:
            account = web3.eth.getBalance(block_chain_id)
        except Exception as e:
            raise api_utils.BadRequest(ast.literal_eval(str(e))[0])
        return Response({'my_balance':account},status=HTTP_200_OK)