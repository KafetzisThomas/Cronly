from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created! You're now able to login.")
            return redirect('users:login')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})
