from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions

from api.serializers import UserSerializer, GroupSerializer, PostSerializer, ProfileSerializer, PostPictureCRUDSerializer
from api.permissions import AuthorAndStaffEdit, NoDeletePermission, DenyAccesToOtherUsersProfiles, AllowCreateProfileWithoutAuthentication, UpdateOrDeleteOnly

from users.models import Profile
from blog.models import Post, PostPicture


import boto3
from botocore.client import Config
from DjangoBlogTutorial import settings

def get_upload_pics_url(filename):
        s3_signature ={
            'v4':'s3v4',
            'v2':'s3'
        }
        client = boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version=s3_signature['v4']),
            region_name='us-east-1'
        )
        url = client.generate_presigned_url('put_object',
                                              Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                      'Key': filename,
                                                      'ACL': 'public-read'
                                                      },
                                              ExpiresIn=100000)
        return url

def createUploadLink(request):
    filename = request.GET['filename']
    return JsonResponse ({'url': get_upload_pics_url(filename) })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [ NoDeletePermission, DenyAccesToOtherUsersProfiles | AllowCreateProfileWithoutAuthentication]
    def get_queryset(self):
        get_self = self.request.query_params.get('self')
        if get_self:
            return self.queryset.filter(user_id=self.request.user.id)
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user_id=self.request.user.id)
            

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    permission_classes = [AuthorAndStaffEdit, permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        res = self.request.query_params.get('author')
        if res:
            return self.queryset.filter(author__username=res)
        return self.queryset

class PostPicViewSet(viewsets.ModelViewSet):
    queryset = PostPicture.objects.all()
    serializer_class = PostPictureCRUDSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UpdateOrDeleteOnly]