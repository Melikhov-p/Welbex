from django.db import models
from django.core.validators import MaxValueValidator
import csv
import os


class Location(models.Model):
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    zip_code = models.CharField(max_length=256, unique=True, db_index=True, null=False, blank=False)
    lat = models.CharField(max_length=256)
    lng = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.zip_code

    @staticmethod
    def load_csv_locations():
        try:
            with open('app/utils/uszips.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    Location.objects.get_or_create(zip_code=row[0], city=row[3], state=row[5], lat=row[1], lng=row[2])
        except Exception as e:
            print(str(e))


class Cargo(models.Model):
    pickup_location = models.ForeignKey(Location, related_name='cargo_pickup', on_delete=models.PROTECT)
    delivery_location = models.ForeignKey(Location, related_name='cargo_delivery', on_delete=models.PROTECT)
    weight = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(1000)])
    description = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'

    def __str__(self):
        return str(self.id)


class Car(models.Model):
    number = models.CharField(max_length=5, unique=True, db_index=True, null=False, blank=False)
    current_location = models.ForeignKey(Location, related_name='car_location', on_delete=models.PROTECT)
    carrying = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(1000)])

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return self.number
