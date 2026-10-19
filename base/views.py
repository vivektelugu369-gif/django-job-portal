from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.
@login_required(login_url='login_')
def home(request):
    recent_jobs = Job.objects.all().order_by('-id')[:4]
    return render(request,'home.html',{'recent_jobs':recent_jobs})

def jobs(request):
    data = Job.objects.all()
#---------------------------------------------------------------------
    query = request.GET.get('q','')
    location = request.GET.get('location','')
    if query:
        data = data.filter(Q(title__icontains=query)|Q(company__icontains=query)|Q(required_skills__icontains=query))
    if location:
        data = data.filter(location__icontains=location)
#---------------------------------------------------------------------
    job_type = request.GET.get('job_type','')
    if job_type:
        data = data.filter(job_type__iexact=job_type)
    return render(request,'jobs.html',{'data':data,'query':query,'location':location,'job_type':job_type})

def job_details(request,id):
    job_data = get_object_or_404(Job, pk=id)
    return render(request,'job_details.html',{'job_data':job_data})

@login_required
def apply_job(request,id):
    selected_job = get_object_or_404(Job,pk=id)
    application, created = JobApplication.objects.get_or_create(
        application = request.user,
        job = selected_job
    )
    if created:
        messages.success(request,'Your application was submitted successfully!')
    else:
        messages.error(request,'You have already applied for this job!')
    return redirect('job_details',id=id)

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(application = request.user).select_related('job').order_by('-applied_at')
    return render(request,'my_applications.html',{'applications':applications})

@login_required(login_url='login_')
def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        description = request.POST.get('description')
        required_skills = request.POST.get('required_skills')
        Job.objects.create(
            title = title,
            company = company,
            location = location,
            job_type = job_type,
            salary = salary if salary else None,
            description = description,
            required_skills = required_skills,
            posted_by = request.user                         # editiong and deleting jobs bythe user who posted it
        )
        messages.success(request,'Job Posted successfully!')
        return redirect('jobs')
    return render(request,'post_job.html')


@login_required(login_url='login_')
def edit_job(request,id):
    job_data = get_object_or_404(Job,id=id,posted_by=request.user)
    if request.method == 'POST':
        job_data.title = request.POST['title']
        job_data.company = request.POST['company']
        job_data.location = request.POST['location']
        job_data.job_type = request.POST['job_type']
        salary = request.POST.get('salary')
        job_data.salary = request.POST['salary']
        job_data.description = request.POST['description']
        job_data.required_skills = request.POST['required_skills']
        job_data.save()
        messages.success(request,'job updated successfully!')
        return redirect('jobs')
    return render(request,'edit_job.html',{'job':job_data})


@login_required(login_url='login_')
def delete_job(request,id):
    job_data = get_object_or_404(Job,id=id,posted_by = request.user)
    if request.method == 'POST':
        job_data.delete()
        messages.success(request,'job deleted successfuly!')
        return  redirect('jobs')
    return render(request,'delete_job.html',{'job':job_data})


@login_required(login_url='login_')
def job_applicants(request,id):
    job_data = get_object_or_404(Job,id=id,posted_by=request.user)
    applications = JobApplication.objects.filter(job = job_data).select_related('application')
    return render(request,'job_applicants.html',{'job':job_data,'applications':applications})

@login_required(login_url='login_')
def update_application_status(request,id):
    application = get_object_or_404(JobApplication,id=id,job__posted_by=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['Pending','Accepted','Rejected']:
            application.status = status
            application.save()
            messages.success(request,'Application status updated successfully')
        else:
            messages.error(request,'Invalid Application status')
            return redirect('job_applicants',id=application.job.id)
    return redirect('job_applicants',id=application.job.id)

def about(request):
    return render(request,'about.html')