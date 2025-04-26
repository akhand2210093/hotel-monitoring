from django.urls import path
from . import views

urlpatterns = [
    path("trigger_report/", views.TriggerReportView.as_view(), name="trigger_report"),
    path("get_report/<str:report_id>/", views.GetReportView.as_view(), name="get_report"),
]