from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .handlers.add_order import handle_add_order
from .handlers.delete_order import handle_delete_order
from .handlers.modals import get_modals
from .handlers.search_order import handle_search_order
from .handlers.total_paid import handle_total_paid_orders
from .handlers.update_status import handle_update_status
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


def order_detail_view(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "order_items__menu_item",
        ),
        id=order_id,
    )

    context = {"order": order}
    return render(request, "orders/order_detail.html", context)
