from django.urls import path
from .views import *

urlpatterns = [
    path('',register,name='register'),
    path('login_',login_,name='login_'),
    path('logout_',logout_,name='logout_'),
    path('profile',profile,name='profile'),
    path('forget_pasw',forget_pasw,name='forget_pasw'),
    path('reset_pasw',reset_pasw,name='reset_pasw'),
    path('update_pro.html',update_pro,name='update_pro')
]