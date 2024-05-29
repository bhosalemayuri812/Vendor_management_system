# vendors/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_on_save(sender, instance, **kwargs):
    vendor = instance.vendor
    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
    total_orders = purchase_orders.count()
    on_time_orders = purchase_orders.filter(status='completed', delivery_date__lte=models.F('delivery_date')).count()
    avg_quality = purchase_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    avg_response_time = purchase_orders.exclude(acknowledgment_date=None).aggregate(
        avg_time=models.Avg(models.F('acknowledgment_date') - models.F('issue_date'))
    )['avg_time'].total_seconds() / 3600 if total_orders else 0
    fulfillment_rate = purchase_orders.filter(status='completed').count() / total_orders if total_orders else 0

    vendor.on_time_delivery_rate = on_time_orders / total_orders if total_orders else 0
    vendor.quality_rating_avg = avg_quality
    vendor.average_response_time = avg_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate,
    )

@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_performance_on_delete(sender, instance, **kwargs):
    update_vendor_performance_on_save(sender, instance)
