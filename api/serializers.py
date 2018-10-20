from rest_framework import fields, serializers
from .models import UserBase

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
            'birthday','avatar_url', 'first_name','last_name')


class UserWithTokenSerializer(UserSerializer):
    token = serializers.CharField(read_only=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('token',)