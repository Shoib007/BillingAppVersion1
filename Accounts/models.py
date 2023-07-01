from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    createAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

class User(AbstractUser):
    waiter = "Waiter"
    admin = "Admin"
    chef = "Chef"
    cashier = "Cashier"
    ROLE = (
        (waiter, waiter),
        (admin, admin),
        (chef, chef),
        (cashier, cashier)
    )

    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE, default="Waiter", blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username



class Profile(models.Model):
    waiter = "Waiter"
    admin = "Admin"
    chef = "Chef"
    cashier = "Cashier"
    ROLE = (
        (waiter, waiter),
        (admin, admin),
        (chef, chef),
        (cashier, cashier)
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE, default="Waiter", blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.branch}'
 


class Customer(models.Model):
    name = models.CharField(max_length=255, default="No Name")
    contact = models.IntegerField(null=True, blank=True)
    address = models.TextField(max_length=300)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name


@receiver(signal=post_save, sender=User)
def profileCreator(sender, instance, created, *args, **kwargs):
    if created and instance.role == 'Admin':
        instance.superUser()

