from django.shortcuts import render
from django.http import HttpResponse
#from rest_framework.response import Response
from rest_framework import serializers, viewsets
from .models import Post, User, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
#from rest_framework.decorators import api_viewd


# Create your views here.

def index(request):
    context ={
        "posts":[
            {"name":"post1", "content":"content1"},
            {"name":"post2", "content":"content2"}
        ]
    }
    
    return render(request, "index.html", context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
