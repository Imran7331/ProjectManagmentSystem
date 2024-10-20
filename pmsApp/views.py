# views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Project, Task, User
from .serializers import ProjectSerializer, TaskSerializer, CreateNewPrimaryUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# User Registration View
class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateNewPrimaryUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    # Define the queryset attribute
    queryset = Project.objects.all()  # Add this line

    def get_queryset(self):
        # Override this method to filter out soft-deleted projects
        return self.queryset.filter(is_deleted=False)

    def perform_destroy(self, instance):
        # Soft delete by marking as deleted
        instance.is_deleted = True
        instance.save()

    def perform_create(self, serializer):
        # Set the owner to the currently authenticated user
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    # Define the queryset attribute
    queryset = Task.objects.all()  # Add this line

    def get_queryset(self):
        # Modify this method if you need to filter tasks in any way
        return self.queryset.filter(is_deleted=False)  # Adjust according to your model

    def perform_destroy(self, instance):
        # Soft delete logic
        instance.is_deleted = True
        instance.save()

    def perform_create(self, serializer):
        # Assign the current user as the owner if applicable
        serializer.save(owner=self.request.user)
