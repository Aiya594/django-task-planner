from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project,Task,Comment
from .serializers import ProjectSerializer,TaskSerializer,CommentSerializer
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "deadline", "priority"]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]

        if project.owner != self.request.user:
            raise PermissionDenied("You cannot add tasks to this project.")

        serializer.save()

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = "done"
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter()
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)