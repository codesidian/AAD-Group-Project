from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    name = models.CharField(max_length=56)
    charge_code = models.CharField(max_length=16)
    pays_vat = models.BooleanField()
    allowed_chemicals = models.BooleanField()
    enabled = models.BooleanField()
    department_id = models.ForeignKey(
      'Department',
      on_delete=models.PROTECT
    )


class Department(models.Model):
    name = models.CharField(max_length=56)
    head_id = models.ForeignKey(
      'Customer',
      on_delete=models.PROTECT
    )


class Item(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=3, decimal_places=2)
    quantity = models.PositiveIntegerField()
    warning_quantity = models.PositiveIntegerField()
    is_chemical = models.BooleanField()
    pack_size = models.PositiveSmallIntegerField()
    for_sale = models.BooleanField(default=True)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        TO_ORDER = 'TO', _('To Order')
        ON_ORDER = 'ON', _('On Order')
        CANCELLED = 'CA', _('Cancelled')
        COMPLETED = 'CO', _('Completed')

    item_id = models.ForeignKey(
        'Item',
        on_delete=models.PROTECT
    )
    datetime = models.DateTimeField()
    staff_id = models.ForeignKey(
        'Staff',
        on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.TO_ORDER
    )


class Return(models.Model):
    class ReturnReason(models.TextChoices):
        DAMAGED = 'DA', _('Damaged')
        NOT_NEEDED = 'NN', _('Not Needed')
        WRONG_ITEM = 'WI', _('Wrong Item')

    datetime = models.DateTimeField()
    staff_id = models.ForeignKey(
        'Staff',
        on_delete=models.PROTECT
    )
    customer_id = models.ForeignKey(
        'Customer',
        on_delete=models.PROTECT
    )
    sale_item_id = models.ForeignKey(
        'SaleItem',
        on_delete=models.PROTECT
    )
    reason = models.CharField(
        max_length=2,
        choices=ReturnReason.choices
    )
    quantity = models.PositiveIntegerField()


class Sale(models.Model):
    datetime = models.DateTimeField()
    customer_id = models.ForeignKey(
        'Customer',
        on_delete=models.PROTECT
    )


class SaleItem(models.Model):
    sale_id = models.ForeignKey(
        'Sale',
        on_delete=models.CASCADE
    )
    item_id = models.ForeignKey(
        'Item',
        on_delete=models.PROTECT
    )
    price_at_sale = models.DecimalField(max_digits=3, decimal_places=2),
    quantity = models.PositiveIntegerField()
    returned_quantity = models.PositiveIntegerField()


class Staff(models.Model):
    class StaffAccessLevel(models.TextChoices):
        TRAINEE = 'TR', _('Trainee')
        BASIC = 'BA', _('Basic')
        MANAGER = 'MA', _('Manager')

    name = models.CharField(max_length=56)
    login_code = models.CharField(max_length=16)
    access_level = models.CharField(
        max_length=2,
        choices=StaffAccessLevel.choices,
        default=StaffAccessLevel.TRAINEE
    )
    enabled = models.BooleanField()


class StockCheck(models.Model):
    datetime = models.DateTimeField()
    staff_id = models.ForeignKey(
        'Staff',
        on_delete=models.PROTECT
    )


class StockCheckItem(models.Model):
    stock_check_id = models.ForeignKey(
      'StockCheck',
      on_delete=models.CASCADE
    )
    item_id = models.ForeignKey(
      'Item',
      on_delete=models.PROTECT
    )
    observed_quantity = models.PositiveIntegerField()
    expected_quantity = models.PositiveIntegerField()
