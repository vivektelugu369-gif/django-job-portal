from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    salary = models.IntegerField(null=True,blank=True)
    description = models.TextField()
    required_skills = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='posted_jobs')

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    application = models.ForeignKey(User,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=[
        ('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejeted')
    ],default='Pending')

    def __str__(self):
        return f'{self.application.username} - {self.job.title}'
