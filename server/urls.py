from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    re_path(r"^(js|css|img)\/(.*)$", views.serve),
    # path('node_modules/js-cookie/dist/js.cookie.mjs', views.serve_js_cookie)
]

urlpatterns += [
    path('login/', views.login),
    path('logout/', views.logout),
    path('submit/', views.submit),
    path('check-submit/', views.check_submit)
]