from asyncore import read
from dataclasses import field, fields
import email
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import Profile

from blog.models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source="user.username", read_only=False)
    email = serializers.EmailField(source="user.email", read_only=False)
    password = serializers.CharField(source="user.password", read_only=False)
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'password', 'image']
    

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    date_posted = serializers.DateTimeField()
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'date_posted', 'author_id', 'author_username']
    