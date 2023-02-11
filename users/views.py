from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.models import User

def login_view(request):
    if request.method == 'GET' and request.user.is_authenticated is not True:
        return render(request, 'login.html')
    elif request.method == 'GET' and request.user.is_authenticated is True:
        return redirect('item_list')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('item_list')
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials'})