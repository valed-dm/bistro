from rest_framework import serializers

from bistro.orders.models import Menu
from bistro.orders.models import Order
from bistro.orders.models import OrderItem


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model.

    Serializes all fields of the Menu model for use in API responses and requests.
    """

    class Meta:
        model = Menu
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.

    Serializes the menu item, quantity, and total price of an order item.
    The menu item is represented using the MenuSerializer.
    """

    menu_item = MenuSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Serializes the order details, including the associated order items and total price.
    The order items are represented using the OrderItemSerializer.
    """

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
