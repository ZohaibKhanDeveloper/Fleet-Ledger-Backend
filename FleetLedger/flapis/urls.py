from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard),
    path('vehicles/',views.Vehicles.as_view()),
    path('vehicle/<int:id>/',views.VehicleDetail.as_view()),
    path('drivers/',views.Drivers.as_view()),
    path('driver/<int:id>/',views.DriverDetail.as_view()),
    path('trips/',views.Trips.as_view()),
    path('trip/<int:id>/',views.TripDetail.as_view()),
    path('payrolls/',views.Payrolls.as_view()),
    path('payroll/<int:id>/',views.PayrollDetail.as_view()),
    path('driver/vehicle/options/',views.vehicle_driver_options),
    path('trip/detail/report/',views.detail_trips_report),
    path('driver/<int:id>/report/',views.summarized_driver_report),
    path('driver/<int:id>/trips/report/',views.detail_driver_trips_report),
]
