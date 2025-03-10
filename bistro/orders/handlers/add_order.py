from django.contrib import messages
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect

from bistro.orders.forms import OrderForm
from bistro.orders.models import OrderItem


def handle_add_order(request: HttpRequest) -> HttpResponse | None:
    """
    Handles the addition of a new order based on the submitted form data.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        Optional[HttpResponse]: Redirects to the manager view on success,
        or None if the form is invalid or an error occurs.
    """
    form = OrderForm(request.POST)
    if form.is_valid():
        try:
            with transaction.atomic():
                order = form.save(commit=False)
                order.save()

                items = form.cleaned_data["items"]
                quantities = form.cleaned_data["quantities"]

                order_items = [
                    OrderItem(order=order, menu_item=item, quantity=quantities[item.id])
                    for item in items
                ]
                OrderItem.objects.bulk_create(order_items)
                messages.success(
                    request,
                    f"Order for table {form.cleaned_data['table_number']} "
                    f"added successfully.",
                )
                return redirect("orders:manager")

        except IntegrityError as e:
            messages.error(request, f"An error occurred while saving the order: {e!s}")
        except Exception as e:  # noqa: BLE001
            messages.error(request, f"An unexpected error occurred: {e!s}")

    else:
        messages.error(
            request,
            "Invalid form data. Please check the input and try again.",
        )
    return None
