# Generated by Django 5.0.12 on 2025-03-08 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Course_name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menu',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(verbose_name='Table_number')),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('ready', 'Ready'), ('paid', 'Paid')], default='waiting', max_length=10, verbose_name='Order_status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated_at')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.menu', verbose_name='Course')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order')),
            ],
            options={
                'verbose_name': 'Order_item',
                'verbose_name_plural': 'Order_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='orders.OrderItem', to='orders.menu', verbose_name='Courses'),
        ),
    ]
