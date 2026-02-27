from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
    
     # 🔹 Field-level validation
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required")
        
        return value

    # 🔹 Object-level validation
    def validate(self, data):
        content = data.get("content")

        if not content:
            raise serializers.ValidationError("Content cannot be empty")

        return data