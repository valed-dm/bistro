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
from .models import Order
from .models import OrderItem


def order_management_view(request):  # noqa: C901, PLR0912, PLR0915
    orders = Order.objects.all()
    total_paid = None
    show_search_orders = False
    search_mode = False

    if request.method == "POST":
        if "addorder" in request.POST:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)  # Create order but don't save yet
                order.save()  # Save order first

                # Save selected items with their respective quantities
                items = form.cleaned_data["items"]
                quantities = form.cleaned_data["quantities"]

                order_items = [
                    OrderItem(order=order, menu_item=item, quantity=quantities[item.id])
                    for item in items
                ]
                OrderItem.objects.bulk_create(order_items)

                return redirect("orders:manager")

        elif "deleteorder" in request.POST:
            form = DeleteOrderForm(request.POST)
            if form.is_valid():
                try:
                    order = Order.objects.get(id=form.cleaned_data["order_id"])
                    order.delete()
                    return redirect("orders:manager")
                except ObjectDoesNotExist:
                    messages.error(
                        request,
                        "The order you tried to delete does not exist.",
                    )
                    return redirect("orders:manager")  # or some

        elif "searchorder" in request.POST:
            form = SearchOrderForm(request.POST)
            if form.is_valid():
                table_number = form.cleaned_data.get("table_number")
                status = form.cleaned_data.get("status")
                search_date = form.cleaned_data.get("date")  # Mandatory date field

                # Convert to datetime (midnight of the given date)
                search_date_start = timezone.make_aware(
                    datetime.combine(search_date, datetime.min.time()),
                )
                search_date_end = timezone.make_aware(
                    datetime.combine(search_date, datetime.max.time()),
                )

                # Filters: Apply date and optional table number and status filters
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
                show_search_orders = True
                search_mode = True

        if "updatestatus" in request.POST:
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
                    messages.error(
                        request,
                        "The order you tried to update does not exist.",
                    )
                return redirect("orders:manager")

        elif "totalpaidorders" in request.POST:
            form = TotalPaidOrdersForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data["date"]

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
                total_paid = Order.objects.filter(
                    status="paid",
                    created_at__range=[start_datetime, end_datetime],
                ).annotate(
                    total_order_price=Sum(
                        F("order_items__menu_item__price") * F("order_items__quantity"),
                    ),
                ).aggregate(total=Sum("total_order_price"))["total"] or Decimal("0.00")

    context = {
        "orders": orders,
        "total_paid": total_paid,
        "show_search_orders": show_search_orders,
        "search_mode": search_mode,
        "modals": [
            {"id": "addOrderModal", "form": OrderForm(), "title": "Add Order"},
            {
                "id": "deleteOrderModal",
                "form": DeleteOrderForm(),
                "title": "Delete Order",
            },
            {
                "id": "searchOrderModal",
                "form": SearchOrderForm(),
                "title": "Search Order",
            },
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
        ],
    }
    return render(request, "orders/order_management.html", context)


def order_detail_view(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "order_items__menu_item",
        ),
        id=order_id,
    )

    context = {"order": order}
    return render(request, "orders/order_detail.html", context)
