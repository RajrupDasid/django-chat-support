from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from django.conf import settings
from .serializers import MessageSeializer, UserSerializer
from .models import Message
# Create your views here.


class CsrfExemptSessionAuthentication(SessionAuthentication):
  

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSeializer
    allowed_methods = ('GET','POST','HEAD','OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication)
    pagination_class =  MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset =self.queryset.filter(Q(recipient = request.user) | (Q(user=request.user)))
        target = self.queryset.query_params.get('target',None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient =  request.user, user__username= target) |
                Q(recipient__username = target, user=request.user)
            )
        return super(MessageViewSet, self).list(request, *args, **kwargs)
    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(
                Q(recipient=request.user) | Q(user=request.user) |
                Q(pk=kwargs['pk'])
            )
        )
        serializer = self.get_serializer(msg)
        return Response(serializer.data)
        
class UserModelViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    allowed_methods = ('GET','HEAD','OPTIONS')
    pagination_class = None

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super().list(request, *args, **kwargs)