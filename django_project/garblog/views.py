from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context ={
        "posts":[
            {"name":"post1", "content":"content1"},
            {"name":"post2", "content":"content2"}
        ]
    }

return render(request, "index.html", context)
