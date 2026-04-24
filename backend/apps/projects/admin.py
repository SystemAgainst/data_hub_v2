from django.contrib import admin
from .models import Project, Image


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'address', 'description')
    readonly_fields = ('created_at', 'updated_at')

    # Show a nice preview of related images in the form
    filter_horizontal = ('images',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)
