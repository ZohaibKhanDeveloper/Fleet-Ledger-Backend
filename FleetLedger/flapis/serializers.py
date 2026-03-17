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

# The Below Serializers class are developed for specific purpose only (Like For Trips)
class VehicleForTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['plate_number']

class DriverForTripSerialzer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Driver
        fields = ['name']
    def get_name(self,obj):
        return (obj.dr_first_name+" "+obj.dr_last_name)

class TripSerializer(serializers.ModelSerializer):
    vehicle = VehicleForTripSerializer(read_only=True)
    driver = DriverForTripSerialzer(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField(source='driver',queryset=Driver.objects.all(),write_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(source='vehicle',queryset=Vehicle.objects.all(),write_only=True)
    class Meta:
        model = Trip
        fields = [
            'id', 'vehicle', 'driver', 'origin', 'destination', 
            'start_time', 'end_time', 'revenue', 'fuel_cost', 
            'toll_fees', 'other_expenses', 'status','driver_id','vehicle_id'
        ]

class SalaryPayrollSerializer(serializers.ModelSerializer):
    driver = DriverForTripSerialzer(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField(source='driver',queryset=Driver.objects.all(),write_only=True)
    class Meta:
        model = SalaryPayroll
        fields = [
            'id', 'driver', 'month_year', 'trips_completed', 
            'total_commissions', 'fixed_salary', 'net_payable', 'payment_status','driver_id'
        ]   

class VehicleForTripReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['plate_number']

class DriverForTripReportSerialzer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Driver
        fields = ['name','commission_rate'] 
    def get_name(self,obj):
        if obj.dr_first_name and obj.dr_last_name:
            return (obj.dr_first_name+" "+obj.dr_last_name)
        return None    

class TripDetailReportSerializer(serializers.ModelSerializer):
    driver = DriverForTripReportSerialzer(read_only=True)
    vehicle = VehicleForTripReportSerializer(read_only=True)
    class Meta:
        model = Trip
        fields = [
            'vehicle', 'driver', 'origin', 'destination', 
            'start_time', 'end_time', 'revenue', 'fuel_cost', 
            'toll_fees', 'other_expenses', 'status'
        ]

class DriverTripsListReportSerializer(serializers.ModelSerializer):
    vehicle = VehicleForTripReportSerializer(read_only=True)
    start_time = serializers.SerializerMethodField()
    class Meta:
        model = Trip
        fields = [
            'vehicle', 'origin', 'destination', 
            'start_time', 'revenue', 'fuel_cost', 
            'toll_fees', 'other_expenses'
        ]
    def get_start_time(self,obj):
        if obj.start_time:
            return obj.start_time.strftime("%d-%m-%Y %H:%M:%S %p")
        return None    