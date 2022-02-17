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
    password = serializers.CharField(required=False)
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email','password', 'image']
    
    def get_validation_exclusions(self):
        exclusions = super(ProfileSerializer, self).get_validation_exclusions()
        return exclusions + ['password']

    def update(self, instance, validated_data):

        print (validated_data.get('image'))
        updated_user = validated_data.get('user')

        instance.user.username = updated_user.get('username', instance.user.username)
        instance.user.email = updated_user.get('email', instance.user.email)
        
        instance.image.save(content=validated_data.get('image'), name=str(validated_data.get('image')))
        new_password = validated_data.get('password')
        if new_password:
            instance.user.set_password(new_password)
        instance.user.save()
        instance.save()
        return instance
    
    def create(self, validated_data):
        new_user = validated_data.get('user')
        password = validated_data.get('password')
        user=User(username=new_user.get('username'), email = new_user.get('email'))
        user.set_password(password)
        user.save()
        return user.profile

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
    