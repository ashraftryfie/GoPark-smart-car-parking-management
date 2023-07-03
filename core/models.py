from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, Q, F



class User(AbstractUser):
    PERMISSIONS_TYPES = (
        ('Garage Manager', 'Garage Manager'),
        ('Cashier', 'Cashier'),
        ('Customer', 'Customer'),
    )
    permission = models.CharField(max_length=100, choices=PERMISSIONS_TYPES)

    first_name   = models.CharField(max_length=100)
    last_name    = models.CharField(max_length=100)
    email        = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=100)
    avatar       = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class Brand(models.Model):
    name  = models.CharField(max_length=200, null=False)
    model = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name) + ' - ' + str(self.model)


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='users')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)

    plate_number = models.CharField(max_length=100)
    color        = models.CharField(max_length=100)

    def __str__(self):
        return str(self.brand) + ' - ' + str(self.plate_number)


class Floor(models.Model):
    floor_number = models.IntegerField(null=True, blank=True)
    num_of_parks = models.IntegerField(null=True, blank=True)
    busy_parks   = models.IntegerField(null=False, default=0)
    is_free      = models.BooleanField(null=False, default=True)

    def __str__(self):
        return 'Floor '+str(self.floor_number)


class Parking(models.Model):
    car   = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)

    PARKINGS_TYPES = (
        ('Visitor', 'Visitor'),
        ('Reserved', 'Reserved'),
    )
    parking_type = models.CharField(max_length=100, choices=PARKINGS_TYPES)

    entry_date = models.DateField()
    entry_time = models.TimeField()
    end_date   = models.DateField(null=True, blank=True)
    end_time   = models.TimeField(null=True, blank=True)
    cost       = models.IntegerField(null=True, blank=True)

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Finished', 'Finished')
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-entry_date']
        # constraints = [
        #     CheckConstraint(
        #         check = Q(end_date__gte=F('entry_date')), 
        #         name = 'check_start_date',
        #     ),
        # ]

    def __str__(self):
        return 'Parking NO. '+str(self.id)


class Payment(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.SET_NULL, null=True)
    PAYMENT_TYPES = (
        ('Cash', 'Cash'),
        ('MasterCard', 'MasterCard'),
        ('VisaCard', 'VisaCard'),
        ('PayPal', 'PayPal')
    )

    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPES)
