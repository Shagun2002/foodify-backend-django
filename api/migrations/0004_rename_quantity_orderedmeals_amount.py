# Generated by Django 4.2.1 on 2023-05-29 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_customer_postal_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderedmeals',
            old_name='quantity',
            new_name='amount',
        ),
    ]