from app.models import Cargo, Car
from django_filters import rest_framework as filters
from geopy import distance


class CargoWeightFilter(filters.FilterSet):
    max_weight = filters.NumberFilter(field_name='weight', lookup_expr='lte')
    min_weight = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    has_cars_by_distance = filters.CharFilter(method='filter_cars_by_distance')

    def filter_cars_by_distance(self, queryset, name, value):
        if name == 'has_cars_by_distance':
            max_distance = float(value)
            cars = Car.objects.all()
            for cargo in queryset:
                for car in cars:
                    car_cargo_distance = distance.distance(
                        (float(car.current_location.lat), float(car.current_location.lng)),
                        (float(cargo.pickup_location.lat), float(cargo.pickup_location.lng))
                    ).miles
                    if car_cargo_distance > max_distance:
                        queryset = queryset.exclude(id=cargo.id)
            return queryset
        else:
            return queryset

    class Meta:
        model = Cargo
        fields = ('max_weight', 'min_weight', 'has_cars_by_distance')
