from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('main/', run_iris_detection, name='run_iris_detection'),
    path('mainh/',distance,name='distance'),
    path('send_otp/', send_otp, name='send_otp'),
    path('reset_password/', reset_password, name='reset_password'),
]
