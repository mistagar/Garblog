from django.shortcuts import render
from django.http import HttpResponse
#from rest_framework.response import Response
from rest_framework import serializers, viewsets
from .models import Post, User, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer, RegisterSerializer
#from rest_framework.decorators import api_viewd
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


'''def index(request):
    context ={
        "posts":[
            {"name":"post1", "content":"content1"},
            {"name":"post2", "content":"content2"}
        ]
    }
    
    return render(request, "index.html", context)
'''

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

'''@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Logged in successfully."}, status=status.HTTP_200_OK)
    '''
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Logged in successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
