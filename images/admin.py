from django.contrib import admin
from images.models import *

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'total_likes', 'created']
    list_filter = ['created']