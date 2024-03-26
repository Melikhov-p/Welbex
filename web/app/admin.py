from django.contrib import admin
from app.models import Cargo, Car, Location


class CarAdmin(admin.ModelAdmin):
    list_display = ['number', 'current_location', 'carrying']
    list_display_links = ['number']
    list_filter = ['current_location']
    search_fields = ['number']


class CargoAdmin(admin.ModelAdmin):
    list_display = ['pickup_location', 'delivery_location', 'weight', 'description']
    list_filter = ['pickup_location', 'delivery_location', 'weight']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['zip_code', 'city', 'state', 'lat', 'lng']
    list_display_links = ['zip_code']
    list_filter = ['city', 'state']
    search_fields = ['zip_code']


admin.site.register(Cargo, CargoAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Location, LocationAdmin)
