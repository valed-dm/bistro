from datetime import datetime

from django.db.models import F
from django.db.models import Q
from django.db.models import QuerySet
from django.db.models import Sum
from django.http import HttpRequest
from django.utils import timezone

from bistro.orders.forms import SearchOrderForm
from bistro.orders.models import Order


def handle_search_order(request: HttpRequest) -> tuple[QuerySet, bool, bool]:
    """
    Handles the search for orders based on the submitted form data.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        tuple[QuerySet, bool, bool]: A tuple containing:
            - A QuerySet of filtered orders.
            - A boolean indicating whether the form was valid.
            - A boolean indicating whether the search was performed.
    """
    form = SearchOrderForm(request.POST)
    if form.is_valid():
        table_number = form.cleaned_data.get("table_number")
        status = form.cleaned_data.get("status")
        search_date = form.cleaned_data.get("date")

        search_date_start = timezone.make_aware(
            datetime.combine(search_date, datetime.min.time()),
        )
        search_date_end = timezone.make_aware(
            datetime.combine(search_date, datetime.max.time()),
        )

        filters = Q(created_at__range=[search_date_start, search_date_end])
        if table_number:
            filters &= Q(table_number=table_number)
        if status != "all":
            filters &= Q(status=status)

        orders = Order.objects.filter(filters).annotate(
            total_order_price=Sum(
                F("order_items__menu_item__price") * F("order_items__quantity"),
            ),
        )
        return orders, True, True
    return Order.objects.all(), False, False
