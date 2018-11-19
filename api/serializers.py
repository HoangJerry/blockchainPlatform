from rest_framework import fields, serializers
from rest_framework.fields import empty

from .models import *
import api

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = UserBase
        fields = ('block_chain_id','password',)
    def create(self, validated_data):
        if 'password' in validated_data:
            user = UserBase()
            user.set_password(validated_data['password'])
            validated_data['password'] = user.password
        return super(UserSignUpSerializer, self).create(validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    block_chain_id = serializers.CharField(write_only=True)
    message = serializers.CharField(allow_blank=True, required=False)
    class Meta:
        model = UserBase
        fields = ('block_chain_id', 'password','message')


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(read_only=True)

    class Meta:
        model = UserBase
        fields = ('id','username','email','avatar','role','full_name',
            'birthday','avatar_url', 'first_name','last_name','address','phone',
            'emergency_name','emergency_address','emergency_phone','emergency_relationship')


class UserWithTokenSerializer(UserSerializer):
    token = serializers.CharField(read_only=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('token',)

class UserTestHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    name_of_test = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    block_chain = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TestHistory
        fields = '__all__'

    def get_name_of_test(self,obj):
        return obj.get_name_of_test_display()
    def get_status(self,obj):
        return obj.get_status_display()
    def get_block_chain(self,obj):
        temp = []
        try:
            from web3 import Web3
            web3 = Web3(Web3.HTTPProvider("http://localhost:8080/"))
            contract = web3.eth.contract(
                address= "0xd9215202688707f6db47E282e9904bAF448A5F5C",
                abi='''[ { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "testHistoriesAccts", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x04f7f327" }, { "constant": true, "inputs": [], "name": "getBalance", "outputs": [ { "name": "", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x12065fe0" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "balances", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x27e235e3" }, { "constant": false, "inputs": [ { "name": "_money", "type": "uint256" } ], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function", "signature": "0x2e1a7d4d" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_result", "type": "string" } ], "name": "setResult", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x31027970" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_patient", "type": "address" }, { "name": "_price", "type": "uint256" } ], "name": "setTestHistory", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x62a5814e" }, { "constant": false, "inputs": [ { "name": "_id", "type": "uint256" }, { "name": "_start", "type": "uint256" } ], "name": "rating", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0x6df9986a" }, { "constant": true, "inputs": [ { "name": "_id", "type": "uint256" } ], "name": "getTestHistory", "outputs": [ { "name": "", "type": "address" }, { "name": "", "type": "string" }, { "name": "", "type": "uint256" }, { "name": "", "type": "bool" }, { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0xad601c88" }, { "constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function", "signature": "0xd0e30db0" } ]''')
            web3.eth.defaultAccount = self._context['request'].user.username
            temp = contract.functions.getTestHistory(obj.id).call()
        except Exception as e:
            pass
        return temp

class CreateTestHistorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)
    class Meta:
        model = TestHistory
        fields = ('id','name_of_test','price','user')
        extra_kwargs = {'price': {'required': True,'allow_null':False}}

class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestHistory
        fields = ('doctor_star',)
        extra_kwargs = {'doctor_star': {'required': True,'allow_null':False}}

class DoctorUpdateResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestHistory
        fields = ('result',)
        extra_kwargs = {
            'result': {'write_only': True},
        }
