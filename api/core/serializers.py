from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from taggit.models import Tag
from .models import *


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    # because looking not for id, but for username
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ("id", "h1", "title", "slug", "description", 
        "content", "image", "created_at", "author", "tags")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password_verifier = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password_verifier",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password_verifier = validated_data["password_verifier"]
        if password != password_verifier:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field="slug", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "username", "text", "created_date")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
    
    def create(self, data):
        username = data["username"]
        current_username = self.context['request'].user
        if username != current_username:
            raise serializers.ValidationError({"Username": "Username does not belong to current user"})
        comment = Comment(post=data["post"], username=username, text=data["text"])
        comment.save()
        return comment