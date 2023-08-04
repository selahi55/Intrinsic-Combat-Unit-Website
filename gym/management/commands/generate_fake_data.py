from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from datetime import datetime, timedelta
import random

from accounts.models import Contact, Client, Trainer
from ...models import Course

choices = [
    'B', 
    'KB',
    'W',
    'SC',
    'Y', 
    'PT', 
    'K', 
]

class Command(BaseCommand):
    help = "Generates fake data for the models"

    def handle(self, *args, **options):
        fake = Faker()

        start_date = datetime.now().date()
        due_date = start_date + timedelta(days=30)

        Contact.objects.all().delete()
        Trainer.objects.all().delete()
        Client.objects.all().delete()
        # Course.objects.delete()
        for _ in range(11):
            Contact.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                message=fake.text(max_nb_chars=150),
                date=fake.date_between_dates(date_start=start_date, date_end=due_date),
                discipline=random.choice(choices),
            )
            Client.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                date_of_birth=fake.date_between(start_date='-20y', end_date='today'),
                active=True,
                subscription=random.randint(0,3),
                joined=fake.date_this_decade(),
                due_date=due_date,
            )
            Trainer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                date_of_birth=fake.date_between(start_date='-20y', end_date='today'),
                active=True,
                percent=50,
                joined=fake.date_this_decade(),
            )
            # Course.objects.create(
            #     name=fake.name(),
            # )

