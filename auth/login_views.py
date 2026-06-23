from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('siswa:index')
        
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'siswa:index')
            return redirect(next_url)
        else:
            error_message = "Username atau password salah."
            
    return render(request, 'auth/login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('auth:login')
