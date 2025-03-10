from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect

from bistro.orders.forms import DeleteOrderForm
from bistro.orders.models import Order


def handle_delete_order(request: HttpRequest) -> HttpResponse:
    """
    Handles the deletion of an order based on the submitted form data.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        HttpResponse: Redirects to the manager view after attempting to delete
        the order.
    """
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
