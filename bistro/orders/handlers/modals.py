from typing import Any

from bistro.orders.forms import DeleteOrderForm
from bistro.orders.forms import OrderForm
from bistro.orders.forms import SearchOrderForm
from bistro.orders.forms import TotalPaidOrdersForm
from bistro.orders.forms import UpdateStatusForm


def get_modals() -> list[dict[str, Any]]:
    """
    Returns a list of modal configurations, each containing an ID, form, and title.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents
        a modal configuration with keys 'id', 'form', and 'title'.
    """
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
