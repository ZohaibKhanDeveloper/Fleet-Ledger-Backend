from django.urls import path
from . import views
urlpatterns = [
    path('vehicles/',views.Vehicles.as_view()),
    path('vehicle/<int:id>/',views.VehicleDetail.as_view()),
    path('drivers/',views.Drivers.as_view()),
    path('driver/<int:id>/',views.DriverDetail.as_view()),
    path('trips/',views.Trips.as_view()),
    path('trip/<int:id>/',views.TripDetail.as_view()),
]
