from django.contrib import admin
from . import models
from django.utils.html import format_html
# Register your models here.


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name', 'slug')
    list_filter = ('genre_name', 'slug')
    prepopulated_fields = {'slug': ('genre_name',)}
    search_fields = ('genre_name',)
    ordering = ('id',)
    # show_facets = admin.ShowFacets.ALWAYS



@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'cover_preview', 'release_date', 'status', 'publish')
    list_filter = ('author', 'status', 'release_date', 'status', 'genre')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author', 'release_date', 'genre')
    date_hierarchy = 'publish'
    ordering = ('release_date', 'genre', 'status', 'author')
    raw_id_fields = ('genre',)
#     show_facets = admin.ShowFacets.ALWAYS

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="height: 100px;"/>', obj.cover_image.url)
        return "No Image"

    cover_preview.short_description = "Cover Preview"