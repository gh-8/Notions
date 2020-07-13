"""notions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from myapp.views import home_view, notion_detail_view, notion_list_view, notion_create_view, notion_delete_view, notion_action_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('notions', notion_list_view),
    path('create-notion', notion_create_view),
    path('notions/<int:notion_id>', notion_detail_view),
    path('api/notions/action',notion_action_view),
    path('api/notions/<int:notion_id>/delete', notion_delete_view),
]
