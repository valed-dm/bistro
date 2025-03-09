from datetime import datetime
from decimal import Decimal

from django.db.models import F
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import now
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bistro.orders.models import Menu
from bistro.orders.models import Order
from bistro.orders.models import OrderItem

from .serializers import MenuSerializer
from .serializers import OrderSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "order_items__menu_item",
    ).all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """Create a new order with a table number and selected menu items."""
        table_number = request.data.get("table_number")
        menu_items = request.data.get("menu_items", [])  # List of menu item IDs

        order = Order.objects.create(table_number=table_number)
        for item_id in menu_items:
            menu_item = Menu.objects.get(id=item_id)
            OrderItem.objects.create(order=order, menu_item=menu_item)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
    def delete_order(self, request, pk=None):
        """Delete an order by ID."""
        order = self.get_object()
        order.delete()
        return Response({"message": "Order deleted"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search orders by table number or status."""
        table_number = request.query_params.get("table_number")
        status_filter = request.query_params.get("status")

        queryset = self.get_queryset()
        if table_number:
            queryset = queryset.filter(table_number=table_number)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return Response(OrderSerializer(queryset, many=True).data)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        """Update order status (waiting, ready, paid)."""
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status in ["waiting", "ready", "paid"]:
            order.status = new_status
            order.save()
            return Response(OrderSerializer(order).data)

        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def total_paid_orders(self, request):
        """Calculate total sum of all paid orders within a given date range."""
        date = request.query_params.get("start_date", now().date())

        # Convert to datetime (midnight time)
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())

        # Ensure they're timezone-aware
        start_datetime = (
            timezone.make_aware(start_datetime)
            if timezone.is_naive(start_datetime)
            else start_datetime
        )
        end_datetime = (
            timezone.make_aware(end_datetime)
            if timezone.is_naive(end_datetime)
            else end_datetime
        )

        total = Order.objects.filter(
            status="paid",
            created_at__range=[start_datetime, end_datetime],
        ).annotate(
            total_order_price=Sum(
                F("order_items__menu_item__price") * F("order_items__quantity"),
            ),
        ).aggregate(total=Sum("total_order_price"))["total"] or Decimal("0.00")

        return Response({"total_paid": total})
