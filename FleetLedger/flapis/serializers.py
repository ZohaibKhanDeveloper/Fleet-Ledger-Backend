from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vehicle, Driver, Trip, SalaryPayroll

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vin', 'plate_number', 'model_year', 'status', 'current_mileage']
        
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id','dr_first_name','dr_last_name', 'license_number', 'base_salary', 'commission_rate', 'joining_date']

class SalaryPayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayroll
        fields = [
            'id', 'driver', 'month_year', 'trips_completed', 
            'total_commissions', 'fixed_salary', 'net_payable', 'payment_status'
        ]

# The Below Serializers class are developed for specific purpose only (Like For Trips)
class VehicleForTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','plate_number']

class DriverForTripSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id','dr_first_name','dr_last_name']                

class TripSerializer(serializers.ModelSerializer):
    vehicle = VehicleForTripSerializer(read_only=True)
    driver = DriverForTripSerialzer(read_only=True)
    class Meta:
        model = Trip
        fields = [
            'id', 'vehicle', 'driver', 'origin', 'destination', 
            'start_time', 'end_time', 'revenue', 'fuel_cost', 
            'toll_fees', 'other_expenses', 'status'
        ]