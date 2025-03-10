"""
Code snippet from https://github.com/AnjalBam/testing-models/blob/main/helpers/tests.py
Some minor changes in BaseModelFieldTest done.
model_bakery got custom tinymce.models.HTMLField.
"""

from typing import Any

import pytest
from django.core.exceptions import ValidationError
from django.db import models
from model_bakery import baker

DATETIME_FIELDS = (models.DateTimeField, models.DateField, models.TimeField)


def gen_func():
    return "value"


class BaseModelTest:
    model: models.Model = None

    instance_kwargs: dict[str, Any] = {}

    @pytest.fixture
    def instance(self) -> models.Model:
        return baker.make(self.model, **self.instance_kwargs)

    def test_issubclass_model(self) -> None:
        assert issubclass(self.model, models.Model)


class BaseModelFieldTest:
    model: models.Model = None
    field_name: str = None
    verbose_name: str = None
    related_name: str = None
    field_type: models.Field = None

    null: bool = False
    blank: bool = False
    default: Any = models.fields.NOT_PROVIDED
    unique: bool = False
    db_index: bool = False
    auto_now: bool = False
    auto_now_add: bool = False
    max_length: int | None = None
    max_digits: int | None = None
    decimal_places: int | None = None
    min_value: int | None = None
    exclude: str | None = None

    @property
    def field(self):
        return self.model._meta.get_field(self.field_name)  # noqa: SLF001

    def test_field_type(self):
        assert isinstance(self.field, self.field_type)

    def test_is_null(self):
        assert self.field.null == self.null

    def test_is_unique(self):
        assert self.field.unique == self.unique

    def test_is_indexed(self):
        assert self.field.db_index == self.db_index

    def test_is_blank(self):
        assert self.field.blank == self.blank

    def test_default_value(self):
        assert self.field.default == self.default

    def test_max_length(self):
        if not self.max_length:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" has no max_length constraint.",
            )
        assert self.field.max_length == self.max_length

    def test_verbose_name(self):
        if not self.verbose_name:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" has no max_length constraint.",
            )
        assert self.field.verbose_name == self.verbose_name

    def test_related_name(self):
        if not self.related_name:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" has no max_length constraint.",
            )
        assert self.field.related_name == self.related_name

    def test_max_digits(self):
        if not self.max_digits:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" has no max_length constraint.",
            )
        assert self.field.max_digits == self.max_digits

    def test_decimal_places(self):
        if not self.decimal_places:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" has no max_length constraint.",
            )
        assert self.field.decimal_places == self.decimal_places

    def test_min_value_negative(self):
        if not self.min_value:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" negative: no min_length constraint.",
            )
        short_string = "a" * (self.min_value - 1)
        instance = baker.make(self.model)
        setattr(instance, self.field_name, short_string)
        with pytest.raises(ValidationError):
            instance.clean_fields(exclude=self.exclude)

    def test_min_value_positive(self):
        message = "test min_value provided does not match that of db existing"
        if not self.min_value:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" positive: no min_length constraint.",
            )
        min_string = "a" * self.min_value
        instance = baker.make(self.model)
        setattr(instance, self.field_name, min_string)
        try:
            instance.clean_fields(exclude=self.exclude)
        except ValidationError:
            pytest.fail(message)

    def test_auto_now(self):
        if self.field.__class__ not in DATETIME_FIELDS:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" is not a date/time model type.",
            )

        assert self.field.auto_now == self.auto_now

    def test_auto_now_add(self):
        if self.field.__class__ not in DATETIME_FIELDS:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name}"
                f" is not a date/time model type.",
            )

        assert self.field.auto_now_add == self.auto_now_add


class BaseTestFieldRelated(BaseModelFieldTest):
    related_model = None

    def test_has_correct_related_model(self):
        assert self.field.related_model == self.related_model
