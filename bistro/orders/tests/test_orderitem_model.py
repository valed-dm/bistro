from django.db import models

from bistro.orders.models import Menu
from bistro.orders.models import Order
from bistro.orders.models import OrderItem
from bistro.orders.tests.models import BaseModelFieldTest
from bistro.orders.tests.models import BaseModelTest
from bistro.orders.tests.models import BaseTestFieldRelated


class BaseModel:
    model = OrderItem


class TestOrderItemModel(BaseModel, BaseModelTest):
    def test_question_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "order")
        assert hasattr(instance, "menu_item")
        assert hasattr(instance, "quantity")


class TestFieldOrderItemOrder(BaseModel, BaseTestFieldRelated):
    field_name = "order"
    field_type = models.ForeignKey
    related_model = Order
    db_index = True


class TestFieldOrderItemMenuItem(BaseModel, BaseTestFieldRelated):
    field_name = "menu_item"
    field_type = models.ForeignKey
    verbose_name = "Course"
    related_model = Menu
    db_index = True


class TestFieldOrderItemQuantity(BaseModel, BaseModelFieldTest):
    field_name = "quantity"
    field_type = models.PositiveIntegerField
    verbose_name = "Quantity"
    default = 1
