from .models import Post

from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'author', 'title',
            'body', 'total_likes', 'is_liked',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}
        model = Post
