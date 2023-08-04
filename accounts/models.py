from typing import Iterable, Optional
from django.db import models
import datetime
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Person(models.Model):
    first_name    = models.CharField(max_length=100, null=True)
    last_name     = models.CharField(max_length=100, null=True)
    email         = models.EmailField(max_length=125)
    date_of_birth = models.DateField()
    active        = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ( (today.month, today.day) < (dob.month, dob.day) )

class Trainer(Person):
    trainer_id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    percent      = models.DecimalField(max_digits=3, decimal_places=0, default=0, validators=PERCENTAGE_VALIDATOR)
    joined       = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} Percent-{self.percent}%'

class Client(Person):
    class Tiers(models.IntegerChoices):
        SINGLE_CLASS_3 = 0, 'Single Class-3'
        SINGLE_CLASS_5 = 1, 'Single Class-5'
        DOUBLE_CLASSES = 2, 'Double Classes'
        TRIPLE_CLASSES = 3, 'Triple Classes'
    client_id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription       = models.IntegerField(choices=Tiers.choices, default=0)
    joined             = models.DateField()
    due_date           = models.DateField()
    number_of_classes  = models.IntegerField(default=1)

    def overdue(self):
        return self.due_date < datetime.now().date()
    
    def calculate_payment(self):
        if self.subscription == 0:
            return 12000
        elif self.subscription == 1:
            return 15000
        elif self.subscription == 2:
            return 18500
        elif self.subscription == 3:
            return 23000
        else:
            raise ValueError('Invalid Subscription Type')
        
    # def calculate_period(self):

    def save(self, *args, **kwargs):
        # SINGLE CLASSES
        if self.subscription == 0 or self.subscription == 1:
            self.number_of_classes = 1
        # DOUBLE CLASSES
        elif self.subscription == 2:
            self.number_of_classes = 2
        # TRIPLE CLASSES
        elif self.subscription == 3:
            self.number_of_classes = 3
        else:
            raise ValueError('Invalid Subscription Type')
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Disciplines(models.TextChoices):
    BOXING = 'B', 'Boxing'
    MMA_KB = 'KB', 'MMA-KickBoxing'
    MMA_W = 'W', 'MMA-Wrestling'
    STRENGTH = 'SC', 'Strength and Conditioning'
    YOGA = 'Y', 'Yoga'
    PERSONAL_TRAINING = 'PT', 'Personal Training'
    KIDS = 'K', 'Kids'

# Potential Clients
class Contact(models.Model):
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    email        = models.EmailField(max_length=150)
    message      = models.CharField(max_length=150, null=True)
    date         = models.DateField(default=timezone.now)
    discipline   = models.CharField(max_length=2, choices=Disciplines.choices, default=Disciplines.BOXING)
    showed_up    = models.BooleanField(default=False)
    updated      = models.DateTimeField(auto_now=True)
    created      = models.DateTimeField(auto_now_add=True)

class Plan(models.Model):
    pass