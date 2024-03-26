from rest_framework import status, filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from app.models import Cargo, Car, Location
from app.serializers import CargoSerializer, CarSerializer
from django.shortcuts import get_object_or_404
from geopy import distance
from app.filters import CargoWeightFilter
from django_filters.rest_framework import DjangoFilterBackend


class CargoViewSet(ModelViewSet):
    serializer_class = CargoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CargoWeightFilter

    def create(self, request, *args, **kwargs):
        cargo_data = self.request.data
        pick_up = cargo_data.get('pickup_location')
        delivery = cargo_data.get('delivery_location')
        if pick_up and delivery:
            cargo_data['pickup_location'] = Location.objects.get(zip_code=pick_up)
            cargo_data['delivery_location'] = Location.objects.get(zip_code=delivery)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Pick up and delivery locations are required'})
        try:
            cargo = Cargo.objects.create(**cargo_data)
            return Response(status=status.HTTP_201_CREATED, data=CargoSerializer(cargo).data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})

    def update(self, request, *args, **kwargs):
        cargo = get_object_or_404(Cargo, pk=self.kwargs.get('pk'))
        weight = self.request.data.get('weight')
        description = self.request.data.get('description')
        if weight or description:
            try:
                if weight:
                    cargo.weight = weight
                if description:
                    cargo.description = description
                cargo.save()
                return Response(status=status.HTTP_200_OK, data=CargoSerializer(cargo).data)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Weight or description are required'})

    def get_queryset(self):
        queryset = Cargo.objects.all()
        if self.request.query_params.get('car_location'):
            queryset = queryset.filter(available=True)
        return queryset

    def retrieve(self, request, pk=None):
        cargo = get_object_or_404(Cargo, pk=pk)
        serializer = CargoSerializer(cargo)
        cars_objects = Car.objects.all()
        cars = []
        response = serializer.data
        for car in cars_objects:
            car_cargo_distance = distance.distance(
                (float(cargo.pickup_location.lat), float(cargo.pickup_location.lng)),
                (float(car.current_location.lat), float(car.current_location.lng))
            ).miles
            cars.append({car.number: car_cargo_distance})
        response['cars'] = cars
        return Response(response)


class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer

    def get_queryset(self):
        queryset = Car.objects.all()
        return queryset

    def update(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=self.kwargs.get('pk'))
        try:
            car.current_location = Location.objects.get(zip_code=self.request.data.get('current_location'))
            car.save()
            return Response(status=status.HTTP_200_OK, data=CarSerializer(car).data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})
