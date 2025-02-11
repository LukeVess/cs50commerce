# Generated by Django 5.1.6 on 2025-02-07 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_items_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='auctions.bid'),
        ),
    ]
