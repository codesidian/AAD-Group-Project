from django.db import models


class Customer(models.Model):
    Name = models.CharField()
    ChargeCode = models.CharField()
    PaysVAT = models.BooleanField()
    AllowedChemicals = models.BooleanField()
    Enabled = models.BooleanField()
    DepartmentID = models.ForeignKey(
      'Department',
      on_delete=models.PROTECT
    )


class Department(models.Model):
    Name = models.CharField()
    HeadID = models.ForeignKey(
      'Customer',
      on_delete=models.PROTECT
    )


class Item(models.Model):
    Code = models.CharField(max_length=20)
    Name = models.CharField(max_length=50)
    Price = models.DecimalField(max_digits=3, decimal_places=2)
    Quantity = models.PositiveIntegerField()
    WarningQuantity = models.PositiveIntegerField()
    IsChemical = models.BooleanField()
    PackSize = models.PositiveSmallIntegerField()
    ForSale = models.BooleanField(default=True)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        TO_ORDER = 'TO', _('To Order')
        ON_ORDER = 'ON', _('On Order')
        CANCELLED = 'CA', _('Cancelled')
        COMPLETED = 'CO', _('Completed')

    ItemID = models.ForeignKey(
        'Item',
        on_delete=models.PROTECT
    )
    DateTime = models.DateTimeField()
    StaffID = models.ForeignKey(
        'Staff',
        on_delete=models.PROTECT
    )
    Status = models.CharField(
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.TO_ORDER
    )


class Return(models.Model):
    class ReturnReason(models.TextChoices):
        DAMAGED = 'DA', _('Damaged')
        NOT_NEEDED = 'NN', _('Not Needed')
        WRONG_ITEM = 'WI', _('Wrong Item')

    DateTime = models.DateTimeField()
    StaffID = models.ForeignKey(
        'Staff',
        on_delete=models.PROTECT
    )
    CustomerID = models.ForeignKey(
        'Customer',
        on_delete=models.PROTECT
    )
    SaleItemID = models.ForeignKey(
        'SaleItem',
        on_delete=models.PROTECT
    )
    Reason = models.CharField(
        max_length=2,
        choices=ReturnReason.choices,
        default=ReturnReason.TO_ORDER
    )
    Quantity = models.PositiveIntegerField()


class Sale(models.Model):
    DateTime = models.DateTimeField()
    CustomerID = models.ForeignKey(
        'Customer',
        on_delete=models.PROTECT
    )


class SaleItem(models.Model):
    SaleID = models.ForeignKey(
        'Sale',
        on_delete=models.CASCADE
    )
    ItemID = models.ForeignKey(
        'Item',
        on_delete=models.PROTECT
    )
    PriceAtSale = models.DecimalField(max_digits=3, decimal_places=2),
    Quantity = models.PositiveIntegerField()
    ReturnedQuantity = models.PositiveIntegerField()


class Staff(models.Model):
    class StaffAccessLevel(models.TextChoices):
        TRAINEE = 'TR', _('Trainee')
        BASIC = 'BA', _('Basic')
        MANAGER = 'MA', _('Manager')

    Name = models.CharField()
    LoginCode = models.CharField()
    AccessLevel = models.CharField(
        max_length=2,
        choices=StaffAccessLevel.choices,
        default=StaffAccessLevel.TRAINEE
    )
    Enabled = models.BooleanField()


class StockCheck(models.Model):
    DateTime = models.DateTimeField()
    StaffID = models.ForeignKey(
        'Staff',
        on_delete=models.PROTECT
    )


class StockCheckItem(models.Model):
    StockCheckID = models.ForeignKey(
      'StockCheck',
      on_delete=models.CASCADE
    )
    ItemID = models.ForeignKey(
      'Item',
      on_delete=models.PROTECT
    )
    ObservedQuantity = models.PositiveIntegerField()
    ExpectedQuantity = models.PositiveIntegerField()
