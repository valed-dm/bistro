from decimal import Decimal

from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name="Course_name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menu"

    def __str__(self):
        return f"{self.name} - {self.price}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("all", "All"),
        ("waiting", "Waiting"),
        ("ready", "Ready"),
        ("paid", "Paid"),
    ]

    table_number = models.IntegerField(verbose_name="Table_number")
    items = models.ManyToManyField(Menu, through="OrderItem", verbose_name="Courses")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="waiting",
        verbose_name="Order_status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated_at")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table_number})"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    menu_item = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Course",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    class Meta:
        verbose_name = "Order_item"
        verbose_name_plural = "Order_items"

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.menu_item.price * Decimal(self.quantity)
