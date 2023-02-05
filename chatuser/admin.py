from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin, site
from .models import Message


#class MessageModelAdmin(ModelAdmin):
#    readonly_fields = ('timestamp',)
#    search_fields = ('id', 'body', 'user__username', 'recipient__username',)
#    list_display = ('id', 'user', 'recipient', 'timestamp', 'char_count',)
#    list_display_links = ('id',)
#    list_filter = ('user', 'recipient',)
#
#
admin.site.register(Message)
