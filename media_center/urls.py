from django.urls import path
from . import views

app_name = 'media_center'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Галерея
    path('gallery/', views.gallery_folders, name='gallery_folders'),
    path('gallery/<int:folder_id>/', views.gallery_photos, name='gallery_photos'),

    # Литература
    path('literature/', views.literature_levels, name='literature_levels'),
    path('literature/<str:level>/', views.literature_list, name='literature_list'),
    path('literature/view/<int:lit_id>/', views.literature_view, name='literature_view'),

    # Видеоуроки
    path('videolessons/', views.video_levels, name='video_levels'),
    path('videolessons/<str:level>/', views.video_list, name='video_list'),
    path('videolessons/view/<int:video_id>/', views.video_view, name='video_view'),
]
