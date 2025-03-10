from datetime import datetime
from decimal import Decimal

from django.db.models import F
from django.db.models import Sum
from django.utils import timezone

from bistro.orders.forms import TotalPaidOrdersForm
from bistro.orders.models import Order


def handle_total_paid_orders(request):
    form = TotalPaidOrdersForm(request.POST)
    if form.is_valid():
        date = form.cleaned_data["date"]

        start_datetime = timezone.make_aware(
            datetime.combine(date, datetime.min.time()),
        )
        end_datetime = timezone.make_aware(datetime.combine(date, datetime.max.time()))

        total_paid = Order.objects.filter(
            status="paid",
            created_at__range=[start_datetime, end_datetime],
        ).annotate(
            total_order_price=Sum(
                F("order_items__menu_item__price") * F("order_items__quantity"),
            ),
        ).aggregate(total=Sum("total_order_price"))["total"] or Decimal("0.00")

        return total_paid  # noqa: RET504

    return None
