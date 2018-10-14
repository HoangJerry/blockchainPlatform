from rest_framework import fields, serializers
from .models import UserBase

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = UserBase
        fields = ('password',)
    def create(self, validated_data):
        if 'password' in validated_data:
            user = UserBase()
            user.set_password(validated_data['password'])
            validated_data['password'] = user.password
        return super(UserSignUpSerializer, self).create(validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    block_chain_id = serializers.CharField(write_only=True)

    class Meta:
        model = UserBase
        fields = ('block_chain_id', 'password',)

