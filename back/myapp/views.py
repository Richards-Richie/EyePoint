from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from .models import Users
from .serializers import UserSerializer
from django.http import JsonResponse
from django.shortcuts import render
import subprocess
import os
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password  # Import make_password

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json
from django.contrib.auth import get_user_model
User = get_user_model()


# Store OTPs in a dictionary (should be replaced with a more secure storage method like a database)
otp_storage = {}

@api_view(['POST'])
def send_otp(request):
    data = request.data
    email = data.get('email')
    if not email:
        return JsonResponse({'status': 'fail', 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    otp = get_random_string(length=6, allowed_chars='0123456789')
    otp_storage[email] = otp
    
    subject = "OTP from Eyepoint"
    message = f"Your OTP is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def reset_password(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    otp = data.get('otp')
    print(otp)
    if not all([email, password, otp]):
        return JsonResponse({'status': 'fail', 'message': 'Email, password, and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if email not in otp_storage or otp_storage[email] != otp:
        return JsonResponse({'status': 'fail', 'message': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    user.password = make_password(password)
    user.save()
    
    # Clear OTP after successful password reset
    del otp_storage[email]
    
    return JsonResponse({'status': 'success', 'message': 'Password reset successful'})


@api_view(['POST'])
def register(request):
     serializer = UserSerializer(data=request.data)
     print(request.data)
     data = request.data
     username = data.get('username')
     email = data.get('email')
     otp = data.get('otp')
     password = data.get('password')
     if not email:
        return JsonResponse({'status': 'fail', 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
     if email not in otp_storage or otp_storage[email] != otp:
        return JsonResponse({'status': 'fail', 'message': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)
    
     if serializer.is_valid():
       ip_address = request.META.get('REMOTE_ADDR')
       ip_address = request.META.get('HTTP_X_FORWARDED_FOR', ip_address).split(',')[0]
       serializer.validated_data['ipaddress'] = ip_address
       serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
       serializer.save()
       return Response(serializer.data, status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         email = data.get('email')
#         otp = data.get('otp')
#         password = data.get('password')

#         user = User.objects.filter(email=email).first()
#         if user and user.otp == int(otp):
#             user.set_password(password)
#             user.save()
#             return JsonResponse({'message': 'Registration successful'})
#         else:
#             return JsonResponse({'error': 'Invalid OTP'}, status=400)
#     return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['POST'])
def login(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    ip_address = request.META.get('REMOTE_ADDR')
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', ip_address).split(',')[0]
    
    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if check_password(password, user.password):
        user.ipaddress = ip_address
        print(f"New IP address: {ip_address}, Old IP address: {user.ipaddress}")
        user.save()
        
        return JsonResponse({'status': 'success', 'message': 'Logged in successfully', 'ipaddress': ip_address})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)


def run_iris_detection(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Move up to the 'back' folder's parent directory
    parent_dir = os.path.dirname(os.path.dirname(current_dir))

    # Navigate to the 'iris' folder
    iris_dir = os.path.join(parent_dir, 'iris')

#   Define the path to your target file inside 'iris' folder
    target_file = os.path.join(iris_dir, 'iris_detection.py')

    try:
        # Command to run the iris detection script
        result = subprocess.run(['python', target_file], capture_output=True, text=True)
        
        # Capture the output and errors
        output = result.stdout
        errors = result.stderr

        # You can process output and errors as needed
        context = {
            'output': output,
            'errors': errors
        }
    except Exception as e:
        context = {
            'output': '',
            'errors': str(e)
        }

    # Render a template with the result (create this template)
    return render(request, 'result.html', context)


def distance(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))

    distance_dir = os.path.join(parent_dir, 'distance')
    target_file = os.path.join(distance_dir, 'a.py')
    print(target_file)

    # if not os.path.isfile(target_file):
    #     context = {
    #         'output': '',
    #         'errors': f"Target file not found: {target_file}"
    #     }
    #     return render(request, 'result.html', context)

    try:
        print("try")
        result = subprocess.run(['python', target_file], capture_output=True, text=True)
        print("run")
        output = result.stdout
        errors = result.stderr
        context = {
            'output': output,
            'errors': errors
        }
    except Exception as e:
        context = {
            'output': '',
            'errors': str(e)
        }

    return render(request, 'result.html', context)
