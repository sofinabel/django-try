from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [
        ('student', 'Ученик'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='student', verbose_name='Роль')

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

class SchoolClass(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название класса')

    class Meta:
        db_table = 'groups'
        verbose_name = 'Учебный класс'
        verbose_name_plural = 'Учебные классы'

    def __str__(self):
        return self.name

class VideoLesson(models.Model):
    group = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='videos', verbose_name='Класс')
    title = models.CharField(max_length=200, verbose_name='Название')
    video_url = models.URLField(verbose_name='Ссылка на видео')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video_lessons'
        verbose_name = 'Видеоурок'
        verbose_name_plural = 'Видеоуроки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Literature(models.Model):
    group = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='literature', verbose_name='Класс')
    title = models.CharField(max_length=200, verbose_name='Название')
    file_url = models.URLField(verbose_name='Ссылка на файл')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'literature'
        verbose_name = 'Литература'
        verbose_name_plural = 'Литература'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class GalleryFolder(models.Model):
    group = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='gallery_folders',
                              verbose_name='Класс')
    name = models.CharField(max_length=200, verbose_name='Название папки')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery_folders'
        verbose_name = 'Папка галереи'
        verbose_name_plural = 'Папки галереи'
        ordering = ['name']

    def __str__(self):
        return f"{self.group.name} - {self.name}"


class Gallery(models.Model):
    folder = models.ForeignKey(GalleryFolder, on_delete=models.CASCADE, related_name='photos', verbose_name='Папка')
    title = models.CharField(max_length=200, verbose_name='Название')
    image_url = models.URLField(verbose_name='Ссылка на изображение')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery'
        verbose_name = 'Фото'
        verbose_name_plural = 'Галерея'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


