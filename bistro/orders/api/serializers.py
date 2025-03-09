from rest_framework import serializers

from bistro.orders.models import Menu
from bistro.orders.models import Order
from bistro.orders.models import OrderItem


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "table_number",
            "order_items",
            "status",
            "created_at",
            "updated_at",
            "total_price",
        ]
