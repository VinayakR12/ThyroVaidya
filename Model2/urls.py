from django.urls import path
from .views import *

urlpatterns = [
    path("predict/",predict, name="predict"),
    path("upload/",upload_and_predict, name="upload"),
    path("reports/",profile_page, name="profile_page"),
    path("delete/<int:report_id>/",delete_report, name="delete_report"),
    path("download_report/<int:report_id>/",download_report, name="download_report"),
    path('download/<int:report_id>/',download_pdf, name='download_pdf'),
    path('reportanalysis/',reportanalysis,name="reportanalysis")
]



