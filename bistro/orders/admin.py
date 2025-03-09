from django.contrib import admin

from .models import Menu
from .models import Order
from .models import OrderItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    list_filter = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table_number",
        "status",
        "created_at",
        "updated_at",
        "total_price",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("table_number",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(
        description="Total Price",
    )
    def total_price(self, obj):
        return obj.total_price


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity", "total_price")
    list_filter = ("order", "menu_item")
    search_fields = ("order__id", "menu_item__name")

    @admin.display(
        description="Total Price",
    )
    def total_price(self, obj):
        return obj.total_price
