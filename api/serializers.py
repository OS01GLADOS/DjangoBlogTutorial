from asyncore import read
from dataclasses import field, fields
from select import select
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
        fields = ['id', 'username', 'email','password', 'image']

    def update(self, instance, validated_data):

        updated_user = validated_data.get('user')

        instance.user.username = updated_user.get('username', instance.user.username)
        instance.user.email = updated_user.get('email', instance.user.email)

        print(updated_user)
        instance.user.save()
        return instance


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
    