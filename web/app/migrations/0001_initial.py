# Generated by Django 5.0.2 on 2024-03-26 10:58

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=256)),
                ('state', models.CharField(max_length=256)),
                ('zip_code', models.CharField(db_index=True, max_length=256, unique=True)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
            options={
                'verbose_name': 'Локация',
                'verbose_name_plural': 'Локации',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(1000)])),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('delivery_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cargo_delivery', to='app.location')),
                ('pickup_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cargo_pickup', to='app.location')),
            ],
            options={
                'verbose_name': 'Груз',
                'verbose_name_plural': 'Грузы',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(db_index=True, max_length=5, unique=True)),
                ('carrying', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(1000)])),
                ('current_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='car_location', to='app.location')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
    ]
