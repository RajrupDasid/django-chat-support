from django.db import models
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user",related_name="from_user", db_index=True)
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="reipient", related_name="to_user", db_index=True)
    body =  models.TextField('body')
    timestamp = models.DateTimeField('timestamp',auto_now_add=True,editable=False,db_index=True)

    def __str__(self) -> str:

        return f"{str(self.id)}"
    def char_count(self):
        return len(self.body)

    def notify_ws_clients(self):
        notification = {
            'type':'receive_group_messages',
            'message':f"{self.id}"
        }
        channel_layer = get_channel_layer()
        sync_to_async(channel_layer.group_Send)(f"{self.user.id}, {notification}")
        sync_to_async(channel_layer.group_send)(f"{self.recipient.id},{notification} ")
    
    def save(self,*args,**kwargs):
        new = self.id
        self.body = self.body.strip()
        super(Message, self).save(*args,**kwargs)
        if new is None:
            self.notify_ws_clients()
    class Meta:
        app_label = 'core'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = '-timestamp'
