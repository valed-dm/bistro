from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from bistro.orders.forms import DeleteOrderForm
from bistro.orders.models import Order


def handle_delete_order(request):
    form = DeleteOrderForm(request.POST)
    if form.is_valid():
        try:
            idx = form.cleaned_data["order_id"]
            order = Order.objects.get(id=idx)
            order.delete()
            messages.info(request, f"The order #{idx} successfully deleted.")
        except ObjectDoesNotExist:
            messages.error(request, "The order you tried to delete does not exist.")
    return redirect("orders:manager")
