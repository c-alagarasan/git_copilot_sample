from rest_framework import viewsets, mixins
from .models import Employee, Role
from .serializers import EmployeeSerializer, CustomTokenObtainSerializer, RoleSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.core.exceptions import PermissionDenied
from rest_framework import status

class BaseViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    """
    Base viewset that does not include the `partial_update` method.
    """
    pass
class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': EmployeeSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User Created Successfully',
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.save()
        return user
   

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    print("MyTokenOb",serializer_class)
    
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_role = request.user.role  
        print("user_role",user_role)

        if user_role.name != 'Admin':  # replace 'name' with the actual field name for the role's name
            raise PermissionDenied('You do not have permission to create roles.')

        return super().create(request, *args, **kwargs)