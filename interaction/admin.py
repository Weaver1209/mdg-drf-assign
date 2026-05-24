from django.contrib import admin
from .models import Tag, Comment, Attachment, Notification

admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Notification)