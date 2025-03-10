from django.db import models

from bistro.orders.models import Menu
from bistro.orders.tests.models import BaseModelFieldTest
from bistro.orders.tests.models import BaseModelTest
from bistro.orders.tests.models import BaseTestFieldRelated


class BaseModel:
    model = Menu


class TestMenuModel(BaseModel, BaseModelTest):
    def test_question_has_all_attributes(self, instance):
        assert hasattr(instance, "id")
        assert hasattr(instance, "name")
        assert hasattr(instance, "price")


class TestFieldMenuName(BaseModel, BaseModelFieldTest):
    field_name = "name"
    field_type = models.CharField
    verbose_name = "Course_name"
    max_length = 100


class TestFieldMenuPrice(BaseModel, BaseTestFieldRelated):
    field_name = "price"
    field_type = models.DecimalField
    verbose_name = "Price"
    max_digits = 10
    decimal_places = 2
