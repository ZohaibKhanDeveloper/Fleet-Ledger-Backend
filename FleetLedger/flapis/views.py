from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from decimal import Decimal

@api_view(['GET'])
def dashboard(request):
    cache_key = "dashboard_data"
    dashboard_data = cache.get(cache_key)
    if dashboard_data is not None:
        return Response(dashboard_data,status=HTTP_200_OK)
    total_vehicles = Vehicle.objects.all().count()
    on_maintenance_vehicles = Vehicle.objects.filter(status="MAINTENANCE").count()
    drivers = Driver.objects.all()
    salaries_sum = 0
    for driver in drivers:
        salaries_sum += driver.base_salary
    completed_trips = Trip.objects.filter(status="COMPLETED") 
    total_revenue = 0
    total_trips_profit = 0
    for trip in completed_trips:
        total_revenue += trip.revenue
        profit = trip.revenue - (trip.toll_fees + trip.fuel_cost + trip.other_expenses)
        total_trips_profit += profit - (trip.driver.commission_rate * profit)
    cancelled_trips = Trip.objects.filter(status="CANCELLED").count()
    ongoing_trips = Trip.objects.filter(status="ONGOING").count()
    planned_trips = Trip.objects.filter(status="PLANNED").count()
    pending_salaries = SalaryPayroll.objects.filter(payment_status="PENDING").count()
    paid_salaries = SalaryPayroll.objects.filter(payment_status="PAID").count()
    dashboard_data = {
        "total_revenue":total_revenue,
        "total_trips_profit":total_trips_profit,
        "total_vehicles":total_vehicles,
        "on_maintenance_vehicles":on_maintenance_vehicles,
        "total_drivers":drivers.count(),
        "driver_salaries_sum":salaries_sum,
        "completed_trips":completed_trips.count(),
        "ongoing_trips":ongoing_trips,
        "planned_trips":planned_trips,
        "cancelled_trips":cancelled_trips,
        "pending_salaries":pending_salaries,
        "paid_salaries":paid_salaries
    }
    cache.set(cache_key,dashboard_data,timeout=300)
    return Response(dashboard_data,status=HTTP_200_OK)

class Vehicles(APIView):

    def get(self,request):
        try:
            page = int(request.GET.get('page'))
            items = int(request.GET.get('items'))
        except Exception:
            page = 1
            items = 2    
        cache_key = f"vehicles_page_{page}"    
        data = cache.get(cache_key)
        if data is not None:
            return Response(data,status=HTTP_200_OK)
        vehicles = Vehicle.objects.all().order_by('-model_year')
        paginator = Paginator(vehicles,per_page=items)
        data = paginator.get_page(page)
        serializer = VehicleSerializer(data, many=True)
        data = serializer.data
        cache.set(f"vehicles_page_{page}",data,timeout=120)
        return Response(data,status=HTTP_200_OK)
    
    def post(self,request):
        data = request.data
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("vehicles_page_*")
            cache.delete("dashboard_data")
            cache.delete("driver_vehicle_options")
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class VehicleDetail(APIView):

    def get_vehicle(self,id):
        return get_object_or_404(Vehicle,pk=id)  
    
    def put(self,request,id):
        vehicle = self.get_vehicle(id)
        serializer = VehicleSerializer(vehicle,data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("vehicles_page_*")
            cache.delete("dashboard_data")
            cache.delete("driver_vehicle_options")
            return Response({
                "msg":"Updated Successfully",
                "data":serializer.data
            },status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        vehicle = self.get_vehicle(id)
        if vehicle is not None:
            vehicle.delete()
            cache.delete_pattern("vehicles_page_*")
            cache.delete("dashboard_data")
            cache.delete("driver_vehicle_options")
            return Response({"msg":"Deleted Successfully"},status=HTTP_200_OK)

class Drivers(APIView):

    def get(self,request):
        try:
            page = int(request.GET.get('page'))
            items = int(request.GET.get('items'))
        except Exception:
            page = 1
            items = 2
        cache_key = f"drivers_page_{page}"    
        data = cache.get(cache_key)
        if data is not None:
            return Response(data,status=HTTP_200_OK)
        drivers = Driver.objects.all().order_by('-joining_date')
        paginator = Paginator(drivers,per_page=items)
        data = paginator.get_page(page)
        serializer = DriverSerializer(data,many=True)
        cache.set(cache_key,serializer.data,timeout=120)
        return Response(serializer.data,status=HTTP_200_OK)
    
    def post(self,request):
        data  = request.data
        serializer = DriverSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("drivers_page_*")
            cache.delete("dashboard_data")
            cache.delete("driver_vehicle_options")
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
class DriverDetail(APIView):

    def get_object(self,id):
        return get_object_or_404(Driver,pk=id)
    
    def put(self,request,id):
        driver = self.get_object(id=id)
        serializer = DriverSerializer(driver,data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("drivers_page_*")
            cache.delete("dashboard_data")
            cache.delete("driver_vehicle_options")
            return Response({
                "msg":"Updated Successfully",
                "data":serializer.data
            },status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        driver = self.get_object(id=id)
        driver.delete()
        cache.delete_pattern("drivers_page_*")
        cache.delete("dashboard_data")
        cache.delete("driver_vehicle_options")
        return Response({"msg":"Deleted Successfully"},status=HTTP_200_OK)

class Trips(APIView):

    def get(self,request):
        try:
            page = int(request.GET.get('page'))
            items = int(request.GET.get('items'))
        except Exception:
            page = 1
            items = 2
        cache_key = f"trips_page_{page}"    
        data = cache.get(cache_key)
        if data is not None:
            return Response(data,status=HTTP_200_OK) 
        trips = Trip.objects.all().order_by('-start_time')
        paginator = Paginator(trips,per_page=items)
        data = paginator.get_page(page)
        serializer = TripSerializer(data,many=True)
        cache.set(cache_key,serializer.data,timeout=120)
        return Response(serializer.data,status=HTTP_200_OK)  

    def post(self,request):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("trips_page_*")
            cache.delete("dashboard_data")
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)  

class TripDetail(APIView):

    def get_object(self,id):
        return get_object_or_404(Trip,pk=id) 

    def put(self,request,id):
        trip = self.get_object(id)
        # if trip is not None:
        serializer = TripSerializer(trip,data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("trips_page_*")
            cache.delete("dashboard_data")
            return Response({
                    "msg":"Updated Successfully",
                    "data":serializer.data
                },status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        trip = self.get_object(id)    
        trip.delete()
        cache.delete_pattern("trips_page_*")
        cache.delete("dashboard_data")
        return Response({"msg":"Deleted Successfully"},status=HTTP_200_OK)

class Payrolls(APIView):

    def get(self,request):
        try:
            page = int(request.GET.get('page'))
            items = int(request.GET.get('items'))
        except Exception:
            page = 1
            items = 2
        cache_key = f"payrolls_page_{page}"    
        data = cache.get(cache_key)
        if data is not None:
            return Response(data,status=HTTP_200_OK)
        payrolls = SalaryPayroll.objects.all().order_by('-month_year')
        paginator = Paginator(payrolls,per_page=items)
        data = paginator.get_page(page)
        serializer = SalaryPayrollSerializer(data,many=True)
        cache.set(cache_key,serializer.data,timeout=120)
        return Response(serializer.data,status=HTTP_200_OK)
    
    def post(self,request):
        month = request.data["month"]
        year = request.data["year"]
        payroll = SalaryPayroll.objects.filter(driver=request.data["driver_id"],month_year__month=month,month_year__year=year).exists()
        if payroll:
            return Response({"msg":"Driver Detail already exists."},status=HTTP_400_BAD_REQUEST)
        driver = Driver.objects.get(pk=request.data["driver_id"])
        request.data["fixed_salary"] = driver.base_salary
        request.data["month_year"] = f"{year}-{month}-28"
        trips = Trip.objects.filter(driver=request.data["driver_id"],status="COMPLETED",start_time__year=year,start_time__month=month)
        request.data["trips_completed"] = trips.count()
        total_commission = Decimal('0.00')
        for trip in trips:
            profit = trip.revenue - (trip.toll_fees + trip.fuel_cost + trip.other_expenses)
            total_commission += (profit*Decimal(str(driver.commission_rate)))
        request.data["total_commissions"] = round(total_commission,2)
        request.data["fixed_salary"] = driver.base_salary
        request.data["net_payable"] = driver.base_salary + request.data["total_commissions"]
        request.data["payment_status"] = "PENDING"
        del request.data["month"]
        del request.data["year"]
        serializer = SalaryPayrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("payrolls_page_*")
            cache.delete("dashboard_data")
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class PayrollDetail(APIView):

    def get_object(self,id):
        return get_object_or_404(SalaryPayroll,pk=id) 

    def put(self,request,id):
        payroll = self.get_object(id)
        serializer = SalaryPayrollSerializer(payroll,data={
            "payment_status":request.data["payment_status"]
        },partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete_pattern("payrolls_page_*")
            cache.delete("dashboard_data")
            return Response({
                    "msg":"Updated Successfully",
                    "data":serializer.data
                },status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        payroll = self.get_object(id)    
        payroll.delete()
        cache.delete_pattern("payrolls_page_*")
        cache.delete("dashboard_data")
        return Response({"msg":"Deleted Successfully"},status=HTTP_200_OK)
    
@api_view(['GET'])
def vehicle_driver_options(request):
    cache_key = "driver_vehicle_options"
    options = cache.get(cache_key)
    if options is not None:
        return Response(options,status=HTTP_200_OK)
    drivers = Driver.objects.all()
    vehicles = Vehicle.objects.filter(status="AVAILABLE")
    vehicles_options = VehicleForTripSerializer(vehicles,many=True)
    drivers_options = DriverForTripSerialzer(drivers,many=True)
    options = {
        "vehicles":vehicles_options.data,
        "drivers":drivers_options.data
    }
    cache.set(cache_key,options,timeout=300)
    return Response(options,status=HTTP_200_OK)
    
        