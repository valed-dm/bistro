from django.urls import path

from bistro.orders.views import order_detail_view
from bistro.orders.views import order_management_view

app_name = "orders"

urlpatterns = [
    path("", order_management_view, name="manager"),
    path("order/<int:order_id>/", order_detail_view, name="order_detail"),
]
