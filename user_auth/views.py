from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        a = request.POST['fname']
        b = request.POST['lname']
        c = request.POST['email']
        d = request.POST['uname']
        e = request.POST['pasw']
        try:
            user = User.objects.get(username = d)
            return render(request,'register.html',{'error':True})
        except:
            u = User.objects.create(
                first_name = a,
                last_name = b,
                email = c,
                username = d,
            )
            u.set_password(e)
            u.save()
    return render(request,'register.html')

def login_(request):
    if request.method == 'POST':
        a = request.POST['uname']
        b = request.POST['pasw']
        user = authenticate(username = a,password = b)
        if user:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login_')
    return render(request,'login_.html')

def logout_(request):
    logout(request)
    return redirect('login_')

@login_required
def profile(request):
    profile,created = UserProfile.objects.get_or_create(
        user = request.user
    )
    if request.method == 'POST':
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()
    return render(request,'profile.html',{'user':request.user,'profile':profile})

# def forget_pasw(request):
#     if request.method == 'POST':
#         if 'uname' in request.POST:
#             a = request.POST['uname']
#             try:
#                 user = User.objects.get(username=a)
#                 request.sessions['fp_user'] = user.username
#                 return render(request,'forget_pasw.html',{'new':True},{'old':user})
#             except:
#                 return redirect('forget_pasw')

#         if 'npasw' in request.POST:
#             b = request.POST['npasw']
#             c = request.POST['conf_pasw']

#             u = request.sessions.get('fp_user')
#             data = User.objects.get(username=u)

#             if b != c:
#                 return redirect('forget_pasw')
#             if data.check_password(b):
#                 return redirect('forget_pasw')

#             data.set_password(b)
#             data.save()
#             return redirect('login_')
#     return render(request,'forget_pasw.html')

def forget_pasw(request):
    if request.method == 'POST':
        # Step 1: User enters username
        if 'uname' in request.POST:
            uname = request.POST['uname']
            try:
                user = User.objects.get(username=uname)
                request.session['fp_user'] = user.username
                # Pass both flags in one context dictionary
                return render(request, 'forget_pasw.html', {'new': True, 'old': user})
            except User.DoesNotExist:
                messages.error(request, "User not found")
                return redirect('forget_pasw')

        # Step 2: User enters new password
        if 'npasw' in request.POST:
            new_pass = request.POST['npasw']
            conf_pass = request.POST['conf_pasw']

            uname = request.session.get('fp_user')
            if not uname:
                messages.error(request, "Session expired. Try again.")
                return redirect('forget_pasw')

            user = User.objects.get(username=uname)

            if new_pass != conf_pass:
                messages.error(request, "Passwords do not match")
                return redirect('forget_pasw')

            if user.check_password(new_pass):
                messages.error(request, "New password cannot be same as old password")
                return redirect('forget_pasw')

            user.set_password(new_pass)
            user.save()
            messages.success(request, "Password updated successfully. Please login.")
            return redirect('login_')

    # Default page load
    return render(request, 'forget_pasw.html', {'new': False})


# def reset_pasw(request):
#     if request.method == 'POST':
#         if 'opsw' in request.POST:
#             a = request.POST['opsw']
#             user = authenticate(username = request.user,password=a)
#             if user:
#                 return render(request,'reset_pasw.html',{'new':True})
#             else:
#                 return redirect('reset_pasw.html')
#         if 'npsw' in request.POST:
#             b = request.POST['npsw']
#             user = User.objects.get(username=request.user)

#         if b!='conf_pasw':
#             return redirect('reset_pasw')

#         if b.check_password('npsw'):
#             return redirect('reset_pasw')

#         user.set_password(b)
#         user.save()
#         return redirect('login_')
#     return render(request,'reset_pasw.html')


def reset_pasw(request):
    if request.method == 'POST':
        # Step 1: Verify old password
        if 'opsw' in request.POST:
            old_pass = request.POST['opsw']
            user = authenticate(username=request.user.username, password=old_pass)
            if user:
                return render(request, 'reset_pasw.html', {'new': True})
            else:
                messages.error(request, "Old password is incorrect")
                return redirect('reset_pasw')

        # Step 2: Set new password
        if 'npsw' in request.POST:
            new_pass = request.POST['npsw']
            conf_pass = request.POST['conf_pasw']

            user = User.objects.get(username=request.user.username)

            if new_pass != conf_pass:
                messages.error(request, "Passwords do not match")
                return redirect('reset_pasw')

            if user.check_password(new_pass):
                messages.error(request, "New password cannot be same as old password")
                return redirect('reset_pasw')

            user.set_password(new_pass)
            user.save()
            messages.success(request, "Password updated successfully. Please login again.")
            return redirect('login_')

    return render(request, 'reset_pasw.html', {'new': False})


def update_pro(request):
    if request.method == 'POST':
        a = request.POST['fname']
        b = request.POST['lname']
        c = request.POST['uname']
        d = request.POST['email']
        user = request.user
        user.first_name = a
        user.last_name = b
        user.username = c
        user.email = d
        user.save()
        return redirect('profile')

    return render(request,'update_pro.html')