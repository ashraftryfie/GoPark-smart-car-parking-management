from rest_framework import serializers, validators
from core.models import User
from django.contrib.auth import authenticate



# User serializer for registring
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'phone_number', 'avatar')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with this email is already exists"
                    )
                ]
            }
        }

        def createUser(self, validated_data):
            first_name   = validated_data.get('first_name')
            last_name    = validated_data.get('last_name')
            username     = validated_data.get('username')
            email        = validated_data.get('email')
            password     = validated_data.get('password')
            phone_number = validated_data.get('phone_number')
            avatar       = validated_data.get('avatar')
            

            # create the user object
            user = User.objects.create(
                first_name   = first_name,
                last_name    = last_name,
                username     = username,
                email        = email,
                password     = password,
                phone_number = phone_number,
                avatar       = avatar
                
            )
            
            # return user object
            return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')