from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('jobs/',jobs,name='jobs'),
    path('job_details/<int:id>/',job_details,name='job_details'),
    path('apply_job/<int:id>/',apply_job,name='apply_job'),
    path('my_applications/',my_applications,name='my_applications'),
    path('about/',about,name='about'),
    path('post_job/',post_job,name='post_job'),
    path('edit_job/<int:id>/',edit_job,name='edit_job'),
    path('delete_job/<int:id>/',delete_job,name='delete_job'),
    path('job_applicants/<int:id>/',job_applicants,name='job_applicants'),
    path('update_application_status/<int:id>/',update_application_status,name='update_application_status')
]