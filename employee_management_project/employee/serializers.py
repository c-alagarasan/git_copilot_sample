from rest_framework import serializers
from .models import Employee, Role
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


class EmployeeSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field='name', queryset=Role.objects.all())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['username', 'password', 'email', 'phone_number', 'date_of_birth', 'address', 'role']


class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        Employee = get_user_model()

        try:
            employee = Employee.objects.get(username=attrs['username'])
            print("username",employee)
            
        except Employee.DoesNotExist:
            raise serializers.ValidationError('Username does not exist')

        if not employee.check_password(attrs['password']):
            print("pass",employee.check_password(attrs['password']))
            raise serializers.ValidationError('Incorrect password')

        refresh = RefreshToken.for_user(employee)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']