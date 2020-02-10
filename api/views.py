from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .serializers import ItemSerializer, NotificationSerializer
from .models import Item, Notification

from rest_framework.decorators import action
from rest_framework.response import Response

#MAYBE TODO: 
class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [SessionAuthentication, ]
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer
    
#TODO: Specific item details
# receie item code


#TODO: Checkout:
# receive json of basket


#MAYBE TODO: get customer details


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [SessionAuthentication, ]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all().order_by('created_date')
    
    def list(self, request, *args, **kwargs):
        data = Notification.objects.filter(user_id=self.request.user.id,seen=False)
        serializer = NotificationSerializer(data, many=True)
        return Response(serializer.data)
    
    #you can switch the method to get if you want to test using /api/ page
    @action(detail=True, methods=['post'])
    def seen(self, request, pk=None):
        readNotification = Notification.objects.get(id=pk,user_id=self.request.user.id)
        if readNotification is not None:
            readNotification.seen = True
            readNotification.save()
            serializer = NotificationSerializer(readNotification)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

#TODO: 