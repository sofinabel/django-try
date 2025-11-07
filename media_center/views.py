from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, GalleryFolder, Gallery, SchoolClass, Literature, VideoLesson

context = {
        'school_name': 'Школа №1539',
        'address': 'ул.Маломосковская д.7',
        'phone': '+7 (499) 299-15-39',
        'email': '1539@edu.mos.ru'
    }

def index(request):
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('media_center:index')
        else:
            messages.error(request, 'Неверный никнейм или пароль')

    return render(request, 'login.html', context)


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с такой почтой уже существует')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='student'
            )
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('media_center:index')

    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('media_center:index')

def gallery_folders(request):
    folders = GalleryFolder.objects.all().select_related('group')
    context['folders'] = folders
    return render(request, 'gallery_folders.html', context)

def gallery_photos(request, folder_id):
    folder = get_object_or_404(GalleryFolder, id=folder_id)
    photos = Gallery.objects.filter(folder=folder)
    context['photos'] = photos
    context['folder'] = folder
    return render(request, 'gallery_photos.html', context)


def literature_levels(request):
    return render(request, 'literature_levels.html', context)


def literature_list(request, level):
    level_classes = {
        'elementary': ['1А', '1Б', '2А', '2Б', '3А', '3Б', '4А', '4Б'],
        'middle': ['5А', '5Б', '6А', '6Б', '7А', '7Б', '8А', '8Б', '9А', '9Б'],
        'high': ['10А', '10Б', '11А', '11Б']
    }

    level_names = {
        'elementary': 'младшей школы',
        'middle': 'средней школы',
        'high': 'старшей школы'
    }

    class_names = level_classes.get(level, [])
    classes = SchoolClass.objects.filter(name__in=class_names)

    literature = Literature.objects.filter(group__in=classes)

    context.update({
        'literature': literature,
        'level_name': level_names.get(level, '')
    })

    return render(request, 'literature_list.html', context)

def video_levels(request):
    return render(request, 'video_levels.html', context)

def video_list(request, level):
    level_classes = {
        'elementary': ['1А', '1Б', '2А', '2Б', '3А', '3Б', '4А', '4Б'],
        'middle': ['5А', '5Б', '6А', '6Б', '7А', '7Б', '8А', '8Б', '9А', '9Б'],
        'high': ['10А', '10Б', '11А', '11Б']
    }

    level_names = {
        'elementary': 'младшей школы',
        'middle': 'средней школы',
        'high': 'старшей школы'
    }

    class_names = level_classes.get(level, [])
    classes = SchoolClass.objects.filter(name__in=class_names)

    videolesson = VideoLesson.objects.filter(group__in=classes)

    context.update({
        'videolesson': videolesson,
        'level_name': level_names.get(level, '')
    })

    return render(request, 'video_list.html', context)
