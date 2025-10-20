from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Homepage – shows all posts
    path('', views.home, name='home'),

    # 📰 Single post page (with comments)
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # 💬 Comment delete (for author/admin)
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('save/<int:pk>/', views.save_post, name='save_post'),
    path('unsave/<int:pk>/', views.unsave_post, name='unsave_post'),

]
