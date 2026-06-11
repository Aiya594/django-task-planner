from rest_framework import serializers 
from .models import Project,Task,Comment

class ProjectSerializer(serializers.ModelSerializer):
    owner_username=serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model=Project 
        fields=[
            "id",
            "owner_username",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        
        read_only_fields = [
            "id",
            "owner_username",
            "created_at",
            "updated_at",
        ]
    def validate_title(self,value):
        value=value.strip()
        if len(value)<3:
            raise serializers.ValidationError("Project title must contain at least 3 characters.")

        return value
    
class TaskSerializer(serializers.ModelSerializer):
    project_title = serializers.ReadOnlyField(source="project.title")

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "project_title",
            "title",
            "description",
            "status",
            "priority",
            "deadline",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "project_title",
            "created_at",
            "updated_at",
        ]
    
    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Task title must contain at least 3 characters.")
        return value

    def validate(self, attrs):
        status_value = attrs.get("status")
        description = attrs.get("description", "")

        if status_value == Task.Status.DONE and not description.strip():
            raise serializers.ValidationError(
                "Done task should have a description."
            )
        return attrs

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    task_title = serializers.ReadOnlyField(source="task.title")

    class Meta:
        model = Comment
        fields = [
            "id",
            "task",
            "task_title",
            "author_username",
            "text",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "task_title",
            "author_username",
            "created_at",
        ]

    def validate_text(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError("Comment must contain at least 3 characters.")

        return value