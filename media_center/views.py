from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, GalleryFolder, Gallery, SchoolClass, Literature, VideoLesson

def get_context(request):
    return {
        'school_name': 'Школа №1539',
        'address': 'ул.Маломосковская д.7',
        'phone': '+7 (499) 299-15-39',
        'email': '1539@edu.mos.ru',
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None
    }

def index(request):
    context = get_context(request)
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

    context = get_context(request)
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

    context = get_context(request)
    return render(request, 'register.html', context)

def logout_view(request):
    logout(request)
    return redirect('media_center:index')


@login_required(login_url='media_center:login')
def gallery_folders(request):
    folders = GalleryFolder.objects.all().select_related('group')
    context = get_context(request)
    context['folders'] = folders
    return render(request, 'gallery_folders.html', context)


@login_required(login_url='media_center:login')
def gallery_photos(request, folder_id):
    folder = get_object_or_404(GalleryFolder, id=folder_id)
    photos = Gallery.objects.filter(folder=folder)
    context = get_context(request)
    context['photos'] = photos
    context['folder'] = folder
    return render(request, 'gallery_photos.html', context)


@login_required(login_url='media_center:login')
def literature_levels(request):
    context = get_context(request)
    return render(request, 'literature_levels.html', context)


@login_required(login_url='media_center:login')
def literature_list(request, level):
    level_mapping = {
        'elementary': 'Младшая школа',
        'middle': 'Средняя школа',
        'high': 'Старшая школа'
    }

    level_names = {
        'elementary': 'младшей школы',
        'middle': 'средней школы',
        'high': 'старшей школы'
    }

    group_name = level_mapping.get(level)
    school_class = SchoolClass.objects.filter(name=group_name).first()

    if school_class:
        literature = Literature.objects.filter(group=school_class)
    else:
        literature = []

    context = get_context(request)
    context.update({
        'literature': literature,
        'level_name': level_names.get(level, ''),
        'level': level
    })

    return render(request, 'literature_list.html', context)


@login_required(login_url='media_center:login')
def literature_view(request, lit_id):
    """Страница для просмотра/чтения литературы"""
    literature = get_object_or_404(Literature, id=lit_id)
    context = get_context(request)
    context['literature'] = literature
    return render(request, 'literature_view.html', context)


@login_required(login_url='media_center:login')
def video_levels(request):
    context = get_context(request)
    return render(request, 'video_levels.html', context)


@login_required(login_url='media_center:login')
def video_list(request, level):
    level_mapping = {
        'elementary': 'Младшая школа',
        'middle': 'Средняя школа',
        'high': 'Старшая школа'
    }

    level_names = {
        'elementary': 'младшей школы',
        'middle': 'средней школы',
        'high': 'старшей школы'
    }

    group_name = level_mapping.get(level)
    school_class = SchoolClass.objects.filter(name=group_name).first()

    if school_class:
        videos = VideoLesson.objects.filter(group=school_class)
    else:
        videos = []

    print(videos)
    context = get_context(request)
    context.update({
        'videos': videos,
        'level_name': level_names.get(level, ''),
        'level': level
    })

    return render(request, 'video_list.html', context)


@login_required(login_url='media_center:login')
def video_view(request, video_id):
    """Страница для просмотра видео"""
    video = get_object_or_404(VideoLesson, id=video_id)
    context = get_context(request)
    context['video'] = video
    return render(request, 'video_view.html', context)

