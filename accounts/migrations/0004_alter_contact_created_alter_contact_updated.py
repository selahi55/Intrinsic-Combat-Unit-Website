# Generated by Django 4.1.7 on 2023-07-28 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_contact_created_contact_showed_up_contact_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
