from bistro.orders.forms import DeleteOrderForm
from bistro.orders.forms import OrderForm
from bistro.orders.forms import SearchOrderForm
from bistro.orders.forms import TotalPaidOrdersForm
from bistro.orders.forms import UpdateStatusForm


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
