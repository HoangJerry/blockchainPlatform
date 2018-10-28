from rest_framework import fields, serializers
from .models import *

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
    class Meta:
        model = TestHistory
        fields = '__all__'

    def get_name_of_test(self,obj):
        return obj.get_name_of_test_display()
    def get_status(self,obj):
        return obj.get_status_display()

class CreateTestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestHistory
        fields = ('name_of_test','price')
        extra_kwargs = {'price': {'required': True,'allow_null':False}}

class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestHistory
        fields = ('doctor_star',)
        extra_kwargs = {'doctor_star': {'required': True,'allow_null':False}}

class DoctorUpdateResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestHistory
        fields = ('result')
        extra_kwargs = {'doctor_star': {'required': True,'allow_null':False}}