from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Avg
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
        total_orders = purchase_orders.count()
        
        on_time_orders = purchase_orders.filter(status='completed', delivery_date__lte=F('delivery_date')).count()
        avg_quality = purchase_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        
        avg_response_time = purchase_orders.exclude(acknowledgment_date=None).aggregate(
            avg_time=Avg(F('acknowledgment_date') - F('issue_date'))
        )['avg_time']
        
        if avg_response_time:
            avg_response_time = avg_response_time.total_seconds() / 3600  # Convert to hours
        else:
            avg_response_time = 0

        fulfillment_rate = purchase_orders.filter(status='completed').count() / total_orders if total_orders else 0

        return Response({
            'on_time_delivery_rate': on_time_orders / total_orders if total_orders else 0,
            'quality_rating_avg': avg_quality,
            'average_response_time': avg_response_time,
            'fulfillment_rate': fulfillment_rate,
        })

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset
