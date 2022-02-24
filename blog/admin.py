from urllib.response import addbase

from django.contrib import admin
from .models import Post, PostPicture

admin.site.register(Post)
admin.site.register(PostPicture)
