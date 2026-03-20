from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenBlacklistView
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
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
    path('payrolls/report/',views.payrolls_report),
    path('vehicles/report/',views.vehicles_report),
]
