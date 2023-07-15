import uuid

from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    id = models.UUIDField(
        _("Position id"),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    position_name = models.CharField(_("Position name"), max_length=50)

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    def __str__(self) -> str:
        return self.position_name


class Employee(models.Model):
    id = models.UUIDField(
        _("Employee id"),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    full_name = models.CharField(
        _("Full Name"),
        max_length=50,
        validators=[
            validators.RegexValidator(
                r"^[a-zA-Z\s]+$", message=_("Only letters are allowed.")
            )
        ],
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="employee_position",
        blank=True,
        null=True,
        verbose_name=_("Position"),
    )
    hire_date = models.DateField()
    email = models.EmailField()
    supervisor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
        verbose_name=_("Supervisor"),
    )

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")