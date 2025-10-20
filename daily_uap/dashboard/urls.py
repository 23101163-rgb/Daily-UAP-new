from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('author/', views.author_dashboard, name='author_dashboard'),
    path('reader/', views.reader_dashboard, name='reader_dashboard'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('save/<int:pk>/', views.save_post, name='save_post'),
    path('saved_posts/', views.saved_posts, name='saved_posts'),
]
