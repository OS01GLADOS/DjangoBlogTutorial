from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import Profile

from blog.models import Post, PostPicture


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source="user.username", read_only=False)
    email = serializers.EmailField(source="user.email", read_only=False)
    password = serializers.CharField(required=False)
    id = serializers.IntegerField(source="user.id", read_only=True)
    registration_date = serializers.DateTimeField(source="user.date_joined", read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email','password', 'image','registration_date']
    
    def get_validation_exclusions(self):
        exclusions = super(ProfileSerializer, self).get_validation_exclusions()
        return exclusions + ['password']

    def update(self, instance, validated_data):

        print (validated_data.get('image'))
        updated_user = validated_data.get('user')

        instance.user.username = updated_user.get('username', instance.user.username)
        instance.user.email = updated_user.get('email', instance.user.email)
        
        if validated_data.get('image'):
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

class PostPictureCRUDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostPicture
        fields = '__all__'

class PostPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPicture
        fields = ['image', 'image_number']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    date_posted = serializers.DateTimeField(read_only=True)
    pics = serializers.SerializerMethodField()  

    def get_pics(self, obj):
        results = PostPicture.objects.filter(post__id=obj.id)
        return PostPictureSerializer(results, many=True).data


    class Meta:
        model = Post
        fields = ['id','title', 'content', 'date_posted', 'author_id', 'author_username', 'pics', 'upload_pics_url']

    def create(self, validated_data):
        new_post = Post()
        new_post.author = self.context['request'].user
        new_post.title = validated_data.get('title')
        new_post.content = validated_data.get('content')
        new_post.save()
        return new_post

    def update(self, instance, validated_data):
        validated_data
        
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.save()
        return instance
