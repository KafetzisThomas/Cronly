from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created.")
            return redirect('users:login')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})
