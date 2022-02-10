# Generated by Django 4.0.2 on 2022-02-10 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_date_time'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='orderdetail',
            constraint=models.UniqueConstraint(fields=('order', 'product'), name='unique_item'),
        ),
    ]
