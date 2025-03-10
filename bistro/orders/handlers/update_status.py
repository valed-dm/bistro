from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect

from bistro.orders.forms import UpdateStatusForm
from bistro.orders.models import Order


def handle_update_status(request: HttpRequest) -> HttpResponse:
    """
    Handles updating the status of an order based on the submitted form data.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        HttpResponse: Redirects to the manager view after attempting to update
        the order status.
    """
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
