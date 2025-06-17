from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model 

from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        User = get_user_model()
        user = User.objects.create_user(username=username, password=password)
        # ✅ EASY FIX: assign admin role
        user.role = 'admin'
        user.save()
        login(request, user)
        return redirect('/fraud/fraud/dashboard/')
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role != 'admin':
                messages.error(request, "Access denied: Only admin users can log in.")
                return redirect('login')  # Or re-render the login page

            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or '/fraud/fraud/dashboard/'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid credentials")

    next_url = request.GET.get('next', '')
    return render(request, 'users/login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('login')


# Create your views here.
