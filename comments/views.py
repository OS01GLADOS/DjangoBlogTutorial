import json
from datetime import time

from django.conf.urls import url
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from blog.models import Post
from comments.forms import CommentCreateForm
from django.contrib import messages

from users.models import Profile
from .models import Comments


# Create your views here.
def add_comment(request, post_id):
    form = CommentCreateForm(request.POST or None)
    if form.is_valid():
        comment = Comments(content=form.data.get('content'),
                           post_id=get_object_or_404(Post, pk=post_id).id,
                           sender_id=request.user.id)
        comment.save()
        messages.success(request=request, message='comment was added')
    return redirect('post-detail', post_id)


def get_comments(request, post_id):
    date = request.GET.get('time')
    res = []
    if date != 0:
        res = list(
            Comments.objects.filter(post_id=post_id).filter(date_posted__gte=date).values('content',
                                                            'sender__username',
                                                            'date_posted',
                                                            'sender__id'
                                                            )
        )
    for elem in res:
        elem['date_posted'] = elem['date_posted'].strftime(
            '%H:%M %b %d, %Y')
        elem['sender_link'] = reverse('user-posts', kwargs={'username': elem['sender__username']} ),
        elem['sender_pic'] = Profile.objects.get(id=elem['sender__id']).image.url
    response = JsonResponse(json.dumps(res), safe=False)
    return response
