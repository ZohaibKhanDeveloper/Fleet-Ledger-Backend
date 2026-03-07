from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

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
            return Response({
                "msg":"Updated Successfully",
                "data":serializer.data
            },status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        driver = self.get_object(id=id)
        driver.delete()
        cache.delete_pattern("drivers_page_*")
        return Response({"msg":"Deleted Successfully"},status=HTTP_200_OK)

                