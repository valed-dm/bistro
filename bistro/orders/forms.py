from django import forms

from .models import Menu
from .models import Order
from .models import OrderItem


class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    quantities = forms.JSONField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Order
        fields = ["table_number", "items", "quantities"]

    def clean_quantities(self):
        """Ensure quantities are valid and match selected items."""
        quantities = self.cleaned_data.get("quantities", {})
        selected_items = self.cleaned_data.get("items", [])

        # Convert all quantity values to integers and ensure they are > 0
        cleaned_quantities = {
            int(menu_id): int(qty)
            for menu_id, qty in quantities.items()
            if int(qty) > 0
        }

        # Ensure all selected items have a corresponding quantity
        selected_item_ids = {item.id for item in selected_items}
        if not selected_item_ids.issubset(cleaned_quantities.keys()):
            msg = "Each selected item must have a valid quantity."
            raise forms.ValidationError(msg)

        return cleaned_quantities


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity"]


class DeleteOrderForm(forms.Form):
    order_id = forms.IntegerField(label="Order ID")


class SearchOrderForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    table_number = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES, required=False)


class UpdateStatusForm(forms.Form):
    order_id = forms.IntegerField(label="Order ID")
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES)


class TotalPaidOrdersForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
