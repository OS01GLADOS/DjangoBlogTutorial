from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_id>/add_comment', views.add_comment, name='comments-add')
]