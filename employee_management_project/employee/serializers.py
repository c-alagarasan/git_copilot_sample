from rest_framework import serializers
from .models import Employee, Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field='name', queryset=Role.objects.all())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['username', 'password', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address', 'role']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Include the user's role in the token
        token['role'] = user.employee.role.name

        return token
    

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']