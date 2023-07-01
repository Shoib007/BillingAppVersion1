from Accounts.models import User, Branch, Customer
from .models import Order, MenuItem, TransactionTable
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Getting the JWT Login and Refresh token
# class JWTokenCreator(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['email'] = user.email
#         return token



# Registering User with validation and hashed password
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])

    class Meta:
        model = User
        fields = ['email','username','password']
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user



class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTable
        fields = '__all__'