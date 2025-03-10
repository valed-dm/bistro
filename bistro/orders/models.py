from decimal import Decimal

from django.db import models


class Menu(models.Model):
    """
    Represents a menu item with a name and price.

    Attributes:
        name (str): The name of the menu item.
        price (Decimal): The price of the menu item.
    """

    name = models.CharField(max_length=100, verbose_name="Course_name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menu"

    def __str__(self) -> str:
        """
        Returns a string representation of the menu item.

        Returns:
            str: A string in the format "name - price".
        """
        return f"{self.name} - {self.price}"


class Order(models.Model):
    """
    Represents an order with a table number, associated menu items, and status.

    Attributes:
        table_number (int): The number of the table where the order was placed.
        items (ManyToManyField): The menu items associated with the order,
        linked through the OrderItem model.
        status (str): The current status of the order (e.g., waiting, ready, paid).
        created_at (datetime): The timestamp when the order was created.
        updated_at (datetime): The timestamp when the order was last updated.
    """

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

    def __str__(self) -> str:
        """
        Returns a string representation of the order.

        Returns:
            str: A string in the format "Order #id (Table table_number)".
        """
        return f"Заказ #{self.id} (Стол {self.table_number})"

    @property
    def total_price(self) -> float:
        """
        Calculates the total price of the order by summing the total price of
        all associated order items.

        Returns:
            float: The total price of the order.
        """
        return sum(item.total_price for item in self.order_items.all())


class OrderItem(models.Model):
    """
    Represents an item within an order, linking a menu item to an order with
    a specific quantity.

    Attributes:
        order (ForeignKey): The order to which this item belongs.
        menu_item (ForeignKey): The menu item associated with this order item.
        quantity (int): The quantity of the menu item in the order.
    """

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

    def __str__(self) -> str:
        """
        Returns a string representation of the order item.

        Returns:
            str: A string in the format "menu_item.name x quantity".
        """
        return f"{self.menu_item.name} x {self.quantity}"

    @property
    def total_price(self) -> Decimal:
        """
        Calculates the total price of the order item by multiplying
        the menu item's price by the quantity.

        Returns:
            Decimal: The total price of the order item.
        """
        return self.menu_item.price * Decimal(self.quantity)
