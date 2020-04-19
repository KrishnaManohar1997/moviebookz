from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework import status

# Since we have to add Cross-Site Request Forgery value everytime in Postman, just excluded
# This is generally send from FORM while submitting data
@csrf_exempt
@require_http_methods(['POST'])
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            return JsonResponse({'status': True, 'message': 'Login Successful'})
        else:
            return JsonResponse({'status': False, 'message': 'Account is disabled'})
    else:
        return JsonResponse({'status': False, 'message': 'Invalid Credentials, You can register from Registration endpoint'}, status=status.HTTP_401_UNAUTHORIZED)


@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({'status': 'disconnected','message':'You have been logged out successfully'})


@csrf_exempt
def user_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        print(username, password, email)
        user = User.objects.create_user(username, email, password)
        user.save()
        return JsonResponse({"status": "Registration Successful"}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"status": "Only POST method is allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
