from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout
import os
import json
from pathlib import Path
from .models import Pathole

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    # dist_path = os.path.join(BASE_DIR, 'dist')
    # file_name = 'index.html'
    # file_path = os.path.join(dist_path, file_name)
    file_path = os.path.join(BASE_DIR, 'server')
    file_path = os.path.join(file_path, 'index.html')
    with open(file_path, 'r') as file:
        content = file.read()
        response = HttpResponse()
        response.write(content)
        return response

def serve(request, folder, file_name):
    dist_path = os.path.join(BASE_DIR, 'dist')
    if folder == 'js':
        folder_path = os.path.join(dist_path, 'js')
        content_type = 'text/javascript'
    elif folder == 'css':
        folder_path = os.path.join(dist_path, 'css')
        content_type = 'text/css'
    elif folder == 'img':
        folder_path = os.path.join(dist_path, 'img')
        content_type = 'img/png'
    else:
        pass
    
    file_path = os.path.join(folder_path, file_name)

    if folder == 'img':
        with open(file_path, 'rb') as file:
            content = file.read()
            response = HttpResponse()
            response['Content-Type'] = content_type
            response.write(content)
            return response
    else:
        with open(file_path, 'r') as file:
            content = file.read()
            response = HttpResponse()
            response['Content-Type'] = content_type
            response.write(content)
            return response

def login(request):
    length = int(request.headers.get('Content-Length'))
    request_content = json.loads(request.read(length).decode('utf-8'))

    try:
        user_name = request_content["auth"]["user-name"]
        password = request_content["auth"]["password"]
    except KeyError:
        return HttpResponse(status = 400)
    
    if User.objects.filter(username = user_name).exists():
        user = authenticate(username = user_name, password = password)
        if user is not None:
            Login(request, user)
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 403)
    else:
        return HttpResponse(status = 401)

def logout(request):
    Logout(request)
    return HttpResponse(status = 200)

def submit(request):
    if request.user.is_authenticated:
        length = int(request.headers.get('Content-Length'))
        request_content = json.loads(request.read(length).decode('utf-8'))

        try:
            address = request_content["pathole"]["address"]
            size = request_content["pathole"]["size"]
            location = request_content["pathole"]["location"]
        except KeyError:
            return HttpResponse(status = 400)

        district = address
        priority = size
        user = request.user

        pathole = Pathole.create(user, address, size, location, district, priority)
        
        if pathole is not None:
            pathole.save()
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 400)

    else:
        return HttpResponse(status = 401)