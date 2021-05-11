
from django.contrib import admin
from django.urls import path, re_path
from my_github_dash import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # for below paths, use re_path to accomodate presence or absence of end slash in requested url
    re_path(r'^table/{0,1}$', views.table, name='table'),
    re_path(r'^bar/{0,1}$', views.bar_chart, name='bar_chart'),
    re_path(r'^pie/{0,1}$', views.pie_chart, name='pie_chart')
]
