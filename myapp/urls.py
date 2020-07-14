from django.urls import path

from .views import home_view, notion_detail_view, notion_list_view, notion_create_view, notion_delete_view, notion_action_view

urlpatterns = [
    path('', notion_list_view),
    path('action/',notion_action_view),
    path('create/', notion_create_view),
    path('<int:notion_id>/', notion_detail_view),
    path('<int:notion_id>/delete/', notion_delete_view),
]
