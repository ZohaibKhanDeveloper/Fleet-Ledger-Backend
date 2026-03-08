from django.db import models 

class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('MAINTENANCE', 'Maintenance'),
    )
    vin = models.CharField(max_length=17, unique=True)
    plate_number = models.CharField(max_length=15, unique=True)
    model_year = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    current_mileage = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.plate_number} - {self.status}"

class Driver(models.Model):
    dr_first_name = models.CharField(max_length=50)
    dr_last_name = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50, unique=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    joining_date = models.DateField()

    def __str__(self):
        return self.dr_first_name + " " + self.dr_last_name

class Trip(models.Model):
    STATUS_CHOICES = (
        ('PLANNED', 'Planned'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    fuel_cost = models.DecimalField(max_digits=10, decimal_places=2)
    toll_fees = models.DecimalField(max_digits=10, decimal_places=2)
    other_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')

    def __str__(self):
        return f"Trip {self.id} ({self.status})"

class SalaryPayroll(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    )
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    month_year = models.DateField()
    trips_completed = models.IntegerField()
    total_commissions = models.DecimalField(max_digits=12, decimal_places=2)
    fixed_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_payable = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.driver} - {self.month_year.strftime('%B %Y')}"