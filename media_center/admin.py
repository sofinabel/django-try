from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SchoolClass, VideoLesson, Literature, GalleryFolder, Gallery


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Роль', {'fields': ('role',)}),
    )


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'created_at']
    list_filter = ['group', 'created_at']
    search_fields = ['title']


@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'created_at']
    list_filter = ['group', 'created_at']
    search_fields = ['title']


@admin.register(GalleryFolder)
class GalleryFolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'created_at']
    list_filter = ['group', 'created_at']
    search_fields = ['name']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_folder', 'get_group', 'created_at']
    list_filter = ['folder__group', 'created_at']
    search_fields = ['title', 'folder__name']

    def get_folder(self, obj):
        return obj.folder.name

    get_folder.short_description = 'Папка'

    def get_group(self, obj):
        return obj.folder.group.name

    get_group.short_description = 'Класс'