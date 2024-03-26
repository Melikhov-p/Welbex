from rest_framework import serializers
from geopy.distance import geodesic
from app.models import Location, Cargo, Car
from django.conf import settings


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    near_cars_amount = serializers.SerializerMethodField()
    pickup_location = serializers.CharField(source='pickup_location.zip_code')
    delivery_location = serializers.CharField(source='delivery_location.zip_code')

    def get_near_cars_amount(self, instance: Cargo):
        near_cars_amount = 0
        cars = Car.objects.all()
        for car in cars:
            distance = geodesic(
                (float(instance.pickup_location.lat), float(instance.pickup_location.lng)),
                (float(car.current_location.lat), float(car.current_location.lng))
            ).miles
            if distance <= settings.NEAR_DISTANCE_FOR_CARS:
                near_cars_amount += 1
        return near_cars_amount

    class Meta:
        model = Cargo
        fields = ('id', 'pickup_location', 'delivery_location', 'weight', 'description', 'near_cars_amount')


class CarSerializer(serializers.ModelSerializer):
    current_location = serializers.CharField(source='current_location.zip_code')

    class Meta:
        model = Car
        fields = '__all__'
