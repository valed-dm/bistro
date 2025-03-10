from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from .forms import DeleteOrderForm
from .forms import OrderForm
from .forms import SearchOrderForm
from .forms import TotalPaidOrdersForm
from .forms import UpdateStatusForm
from .handlers.add_order import handle_add_order
from .handlers.delete_order import handle_delete_order
from .models import Order


def order_management_view(request):
    orders = Order.objects.all()
    total_paid = None
    show_search_orders = False
    search_mode = False

    if request.method == "POST":
        if "addorder" in request.POST:
            return handle_add_order(request)
        if "deleteorder" in request.POST:
            return handle_delete_order(request)
        if "searchorder" in request.POST:
            orders, show_search_orders, search_mode = handle_search_order(request)
        elif "updatestatus" in request.POST:
            return handle_update_status(request)
        elif "totalpaidorders" in request.POST:
            total_paid = handle_total_paid_orders(request)

    context = {
        "orders": orders,
        "total_paid": total_paid,
        "show_search_orders": show_search_orders,
        "search_mode": search_mode,
        "modals": get_modals(),
    }
    return render(request, "orders/order_management.html", context)


def handle_search_order(request):
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


def handle_update_status(request):
    form = UpdateStatusForm(request.POST)
    if form.is_valid():
        order_id = form.cleaned_data["order_id"]
        status = form.cleaned_data["status"]

        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            messages.success(request, "Order status updated successfully.")
        except ObjectDoesNotExist:
            messages.error(request, "The order you tried to update does not exist.")
    return redirect("orders:manager")


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


def get_modals():
    return [
        {"id": "addOrderModal", "form": OrderForm(), "title": "Add Order"},
        {"id": "deleteOrderModal", "form": DeleteOrderForm(), "title": "Delete Order"},
        {"id": "searchOrderModal", "form": SearchOrderForm(), "title": "Search Order"},
        {
            "id": "updateStatusModal",
            "form": UpdateStatusForm(),
            "title": "Update Order Status",
        },
        {
            "id": "totalPaidOrdersModal",
            "form": TotalPaidOrdersForm(),
            "title": "Total Paid Orders",
        },
    ]


def order_detail_view(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "order_items__menu_item",
        ),
        id=order_id,
    )

    context = {"order": order}
    return render(request, "orders/order_detail.html", context)
