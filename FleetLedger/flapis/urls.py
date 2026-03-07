from django.urls import path
from . import views
urlpatterns = [
    path('vehicles/',views.Vehicles.as_view()),
    path('vehicle/<int:id>/',views.VehicleDetail.as_view()),
]
