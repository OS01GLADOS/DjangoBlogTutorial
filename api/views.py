from django.contrib.auth.models import User, Group
from api import serializers
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, PostSerializer
from api.permissions import AuthorAndStaffEdit

from blog.models import Post

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


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