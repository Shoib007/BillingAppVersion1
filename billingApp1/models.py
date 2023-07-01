from django.db import models
from django.utils import timezone
import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from Accounts.models import Customer

class MenuItem(models.Model):
    def imagePath(self, instance = None):
        if instance:
            return os.path.join('FoodImages', instance)
        return None
    
    itemName = models.CharField(max_length=255)
    image = models.ImageField(upload_to=imagePath, blank=True, null=True)
    price = models.CharField(max_length=10)
    discount = models.IntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.itemName} -> {self.id}"

class Table(models.Model):
    order = "ORDER"
    free = "NO ORDER"
    STATUS = (
        (order, order),
        (free, free)
    )
    tableNumber = models.CharField(max_length=3)
    tableStatus = models.CharField(max_length=10, choices=STATUS, default='NO ORDER')
    totalOrder = models.IntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    def increaseOrder(self):
        self.totalOrder += 1
        self.save()
    def resetOrder(self):
        self.totalOrder = 0
        self.save()

    def __str__(self)->str:
        return self.tableNumber


class Order(models.Model):
    pending = 'Pending'
    completed = 'Completed'

    STATUS = (
        (pending, pending),
        (completed, completed)
    )

    cod = "Cash On Delivery"
    card = "Card"
    upi = "UPI Payment"

    PAYMENT_MODE = (
        (cod, cod),
        (card, card),
        (upi, upi)
    )

    paid = "Paid"
    pending = "Pending"

    PAYMENT_STATUS = (
        (paid, paid),
        (pending, pending)
    )

    take_away = "Take Away"
    in_house = "In House"

    TYPE = (
        (take_away, take_away),
        (in_house, in_house)
    )

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null=True)
    tabelNumber = models.ForeignKey(Table, on_delete=models.DO_NOTHING)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE, default="Cash On Delivery")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="Pending")
    order_type = models.CharField(max_length=20, choices=TYPE, default="In House")
    order_status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)


    def order_completed(self):
        self.order_status = "Completed"
        self.save()
    
    def modified_order(self):
        self.updatedAt = timezone.now()
        self.save()
    
    def __str__(self) -> str:
        return str(self.id)
    

class TransactionTable(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subTotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.subTotal}"



@receiver(signal=pre_save, sender=Order)
def handleTable1(sender, instance, *args, **kwargs):
    try:
        orderStatus = instance.order_status
        print("Pre save in Order")
        if orderStatus == 'Pending':
            instance.tabelNumber.increaseOrder()
    except Exception as e:
        print(e)



@receiver(signal=post_save, sender = Order)
def handleTable2(sender, instance, created, *args, **kwargs):
    try:
        paymentStatus = instance.payment_status
        if paymentStatus == "Paid":
            instance.tabelNumber.resetOrder()
    except Exception as e:
        print(e)