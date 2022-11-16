from django.shortcuts import render
from django.http import HttpResponse
import os
from pathlib import Path

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    dist_path = os.path.join(BASE_DIR, 'dist')
    file_name = 'index.html'
    file_path = os.path.join(dist_path, file_name)
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




