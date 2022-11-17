from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout
from django.views.decorators.csrf import ensure_csrf_cookie
import os
import json
from pathlib import Path
from .models import Pathole

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent

@ensure_csrf_cookie
def index(request):
    dist_path = os.path.join(BASE_DIR, 'dist')
    file_name = 'index.html'
    file_path = os.path.join(dist_path, file_name)
    # file_path = os.path.join(BASE_DIR, 'server')
    # file_path = os.path.join(file_path, 'index.html')
    with open(file_path, 'r') as file:
        content = file.read()
        response = HttpResponse()
        response.write(content)
        return response

def serve_js_cookie(request):
    file_path = os.path.join(os.path.join(os.path.join(os.path.join(BASE_DIR, 'node_modules'), 'js-cookie'), 'dist'), 'js.cookie.mjs')
    with open(file_path, 'r') as file:
        content = file.read()
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
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
        with open(file_path, 'r', encoding='utf-8') as file:
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

def check_submit(request):
    if request.user.is_authenticated:
        results = Pathole.objects.filter(user = request.user).values_list('address', 'size', 'location')
        patholes = []
        for result in results:
            pathole = {}
            pathole['address'] = result[0]
            pathole['size'] = result[1]
            pathole['location'] = result[2]
            patholes.append(pathole)
        response_content = {"submit": patholes}
        response = JsonResponse(response_content)
        response.status_code = 200
        return response
    else:
        return HttpResponse(status = 401)