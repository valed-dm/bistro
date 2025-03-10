from django.db import models

from bistro.orders.models import Menu
from bistro.orders.models import Order
from bistro.orders.tests.models import BaseModelFieldTest
from bistro.orders.tests.models import BaseModelTest
from bistro.orders.tests.models import BaseTestFieldRelated


class BaseModel:
    model = Order


class TestOrderModel(BaseModel, BaseModelTest):
    def test_question_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "table_number")
        assert hasattr(instance, "items")
        assert hasattr(instance, "status")
        assert hasattr(instance, "created_at")
        assert hasattr(instance, "updated_at")


class TestFieldOrderTable(BaseModel, BaseModelFieldTest):
    field_name = "table_number"
    field_type = models.IntegerField
    verbose_name = "Table_number"


class TestFieldOrderItems(BaseModel, BaseTestFieldRelated):
    field_name = "items"
    field_type = models.ManyToManyField
    verbose_name = "Courses"
    related_model = Menu


class TestFieldOrderStatus(BaseModel, BaseModelFieldTest):
    field_name = "status"
    field_type = models.CharField
    verbose_name = "Order_status"
    max_length = 10
    default = "waiting"


class TestFieldOrderCreatedAt(BaseModel, BaseModelFieldTest):
    field_name = "created_at"
    field_type = models.DateTimeField
    verbose_name = "Created_at"
    auto_now_add = True
    blank = True


class TestFieldOrderUpdatedAt(BaseModel, BaseModelFieldTest):
    field_name = "updated_at"
    field_type = models.DateTimeField
    verbose_name = "Updated_at"
    auto_now = True
    blank = True
