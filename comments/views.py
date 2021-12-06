from django.http import HttpResponse
from comments.forms import CommentCreateForm
from django.contrib import messages
from . models import Comments


# Create your views here.
def add_comment(request, post_id):
    form = CommentCreateForm(request.POST or None)
    if form.is_valid():
        comment = Comments(content=form.data.get('content'),
                           post_id=post_id,
                           sender_id=request.user.id)
        comment.save()
        messages.success(request=request, message='comment was added')
        return HttpResponse('added successfully')
