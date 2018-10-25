from rest_framework import fields, serializers
from rest_framework.fields import empty

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
        fields = ('id','username','email','avatar',
            'birthday','avatar_url', 'first_name','last_name','address','phone',
            'emergency_name','emergency_address','emergency_phone','emergency_relationship')


class UserWithTokenSerializer(UserSerializer):
    token = serializers.CharField(read_only=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('token',)

class UserTestHistorySerializer(serializers.ModelSerializer):
    name_of_test = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TestHistory
        fields = '__all__'

    def get_name_of_test(self,obj):
        return obj.get_name_of_test_display()
    def get_status(self,obj):
        return obj.get_status_display()


class DoctorRatingSerializer(serializers.ModelSerializer):
    doctor_name          = serializers.CharField()
    doctor_address       = serializers.CharField()
    doctor_phone         = serializers.IntegerField()
    doctor_position      = serializers.CharField(   )
    doctor_hospital_name = serializers.CharField(   )
    doctor_rate          = serializers.IntegerField()
    doctor_comment       = serializers.CharField(   )
    
    class Meta:
        model = DoctorRating
        fields = ('doctor_name', 'doctor_address', 'doctor_phone', 'doctor_position','doctor_hospital_name','doctor_rate','doctor_comment')