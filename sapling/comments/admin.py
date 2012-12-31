from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from models import Comment, CommentConfiguration


class CommentAdmin(GuardedModelAdmin):
    readonly_fields = ('page', 'content',)
    list_display = ('page', 'date', 'commenter', 'content')

admin.site.register(Comment, CommentAdmin)


class CommentConfigurationAdmin(GuardedModelAdmin):
    readonly_fields = ('page',)
    list_display = ('page', 'enabled', 'heading',)

admin.site.register(CommentConfiguration, CommentConfigurationAdmin)