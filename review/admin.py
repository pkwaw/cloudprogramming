from django.contrib import admin
from .models import *
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {'review': ('review',)}

admin.site.register(Review, MarkdownxModelAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Tag, TagAdmin)
