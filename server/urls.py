from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    re_path(r"^(js|css|img)\/(.*)$", views.serve)
]

urlpatterns += [
    path('login/', views.login),
    path('logout/', views.logout),
    path('submit/', views.submit)
]