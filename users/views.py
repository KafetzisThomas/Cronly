from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, UsernameUpdateForm, DiscordWebhookForm

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

@login_required
def account(request):
    user = request.user
    username_form = UsernameUpdateForm(instance=user)
    notification_form = DiscordWebhookForm(instance=user)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_username":
            username_form = UsernameUpdateForm(request.POST, instance=user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Username updated successfully.")
                return redirect("users:account")

        elif action == "update_discord_webhook":
            notification_form = DiscordWebhookForm(request.POST, instance=user)
            if notification_form.is_valid():
                notification_form.save()
                messages.success(request, "Discord Webhook URL updated.")
                return redirect("users:account")

    context = {"username_form": username_form, "notification_form": notification_form}
    return render(request, "users/account.html", context)

@login_required
@require_POST
def delete_account(request):
    user = request.user
    user.delete()
    return redirect("users:register")
