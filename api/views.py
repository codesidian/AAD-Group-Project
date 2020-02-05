from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .serializers import ItemSerializer, NotificationSerializer
from .models import Item, Notification


from rest_framework.response import Response

class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [SessionAuthentication, ]
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [SessionAuthentication, ]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        data = Notification.objects.filter(user_id=self.request.user.id)
        serializer = NotificationSerializer(data, many=True)
        return Response(serializer.data)
