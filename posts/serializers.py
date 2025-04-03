from rest_framework import serializers

from posts.models import Post


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=50)
#     content = serializers.CharField()
#     created_at = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         return Post.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         instance.save()
#         return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "created_at"]
