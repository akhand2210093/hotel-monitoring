from django.shortcuts import render

# Create your views here.
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils.timezone import make_aware
from pytz import timezone
from datetime import timedelta, datetime
import uuid
import os

from .models import StoreStatus, BusinessHour, Timezone, Report
from .serializers import ReportSerializer


class TriggerReportView(APIView):
    def post(self, request):
        report_id = str(uuid.uuid4())
        report = Report.objects.create(report_id=report_id)

        # Trigger report generation asynchronously
        self.generate_report(report)

        return Response({"report_id": report_id}, status=status.HTTP_200_OK)

    def generate_report(self, report):
        try:
            # Load data from the database
            store_status_df = pd.DataFrame(list(StoreStatus.objects.all().values()))
            business_hours_df = pd.DataFrame(list(BusinessHour.objects.all().values()))
            timezones_df = pd.DataFrame(list(Timezone.objects.all().values()))

            # Set default timezone for missing data
            timezones_df["timezone_str"].fillna("America/Chicago", inplace=True)

            # Process data
            report_data = self.process_uptime_downtime(store_status_df, business_hours_df, timezones_df)

            # Save CSV
            file_path = f"reports/report_{report.report_id}.csv"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            report_data.to_csv(file_path, index=False)

            # Update report status
            report.csv_file = file_path
            report.status = "Complete"
            report.save()
        except Exception as e:
            report.status = "Failed"
            report.save()
            print(f"Error generating report: {e}")

    def process_uptime_downtime(self, store_status_df, business_hours_df, timezones_df):
        # Implement your logic for calculating uptime/downtime here
        # This is a placeholder function
        return pd.DataFrame(
            columns=[
                "store_id",
                "uptime_last_hour",
                "uptime_last_day",
                "uptime_last_week",
                "downtime_last_hour",
                "downtime_last_day",
                "downtime_last_week",
            ]
        )

from rest_framework.response import Response
from django.http import FileResponse
from .models import Report
import os

class GetReportView(APIView):
    def get(self, request, report_id):
        try:
            # Fetch the report from the database
            report = Report.objects.get(report_id=report_id)

            # Check report status
            if report.status == "Running":
                return Response({"status": "Running"}, status=200)

            elif report.status == "Complete":
                # Check if the CSV file exists
                if report.csv_file and os.path.exists(report.csv_file.path):
                    file_path = report.csv_file.path
                    return FileResponse(
                        open(file_path, 'rb'),
                        content_type="text/csv",
                        as_attachment=True,
                        filename=f"report_{report_id}.csv"
                    )
                else:
                    return Response({"error": "CSV file not found"}, status=404)
            else:
                # If status is "Failed" or anything else
                return Response({"status": report.status}, status=200)

        except Report.DoesNotExist:
            return Response({"error": "Report not found"}, status=404)
        except Exception as e:
            return Response({"error": f"Internal server error: {str(e)}"}, status=500)
