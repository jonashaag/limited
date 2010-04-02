# coding: utf-8
from django.contrib import admin
from django.utils.translation import ugettext as _

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'edit_time', 'creation_time')
    list_filter = ('isblog', 'public', 'popular', 'in_navigation')
    search_fields = ('title', 'text')
    list_per_page = 20
    prepopulated_fields = {'url': ('title',)}

    fieldsets = (
        (None, {
            'classes' : ('wide',),
            'description' : _("<i>Ctrl+Enter and Ctrl+Shift+Enter</i>: Resize textarea"),
            'fields' : ('user', 'title', 'text', 'url', 'edit_time', 'tags')
        }),
        (_('Post settings'), {
            'classes' : ('collapse', 'wide'),
            'fields' : ('public', 'isblog'),
        }),
        (_('Extra settings'), {
            'classes': ('collapse', 'wide'),
            'fields' : ('popular', 'in_navigation'),
        }),
        (_('Language settings'), {
            'classes': ('collapse', 'wide'),
            'fields' : ('language', 'other_languages'),
        })
    )

    def save_model(self, request, obj, form, change):
        if obj.user is None:
            obj.user = request.user
        obj.save()

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'public']
    list_filter = ['public']

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
