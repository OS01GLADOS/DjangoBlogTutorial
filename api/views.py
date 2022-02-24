from unicodedata import lookup
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api import serializers
from api.serializers import UserSerializer, GroupSerializer, PostSerializer, ProfileSerializer, PostPicSerializer
from api.permissions import AuthorAndStaffEdit, NoDeletePermission, DenyAccesToOtherUsersProfiles, AllowCreateProfileWithoutAuthentication, UpdateOrDeleteOnly

from users.models import Profile
from blog.models import Post, PostPicture

from rest_framework.generics import ListAPIView



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

class PostPicViewSet(ListAPIView):
    queryset = PostPicture.objects.all()
    serializer_class = PostPicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UpdateOrDeleteOnly]
    lookup_field = 'post__id'