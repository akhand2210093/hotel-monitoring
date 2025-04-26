from django.db import models

# Create your models here.
from django.db import models


class StoreStatus(models.Model):
    store_id = models.IntegerField()
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[("active", "Active"), ("inactive", "Inactive")])


class BusinessHour(models.Model):
    store_id = models.IntegerField()
    day_of_week = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()


class Timezone(models.Model):
    store_id = models.IntegerField()
    timezone_str = models.CharField(max_length=100)


class Report(models.Model):
    report_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[("Running", "Running"), ("Complete", "Complete")], default="Running")
    csv_file = models.FileField(upload_to="reports/", null=True, blank=True)
