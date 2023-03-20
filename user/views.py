from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from verify_email.email_handler import send_verification_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.models import UserProfile
from orders.models import Order, OrderDetail
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponseRedirect

def register_request(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            user = form.save()
            userprofile = form.save(commit=False)
            # assign user to your profile
            userprofile.user = user
            userprofile.save()
            login(request, user)
            messages.success(request, f'An email verification has sent! Check your email')
            return redirect('login_prompt')
        messages.warning(request, "Unsuccessful registration. Invalid information.")
    form = UserRegisterForm()
    return render(request=request, template_name="user/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("profile")
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'), )
            else:
                messages.warning(request, "Invalid username or password.")
        else:
            messages.warning(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


def login_prompt(request):
    return render(request, 'user/login_prompt.html')

def password_reset(request):
    return render(request, 'password_reset/recovery_form.html')


@login_required
def profile(request):
    user = request.user
    global userinfo
    userinfo = user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            messages.warning(request, f'Failed to update your details, Kindly retry again. ')
            return redirect('profile')
    else:
        orders = Order.objects.filter(customer_id=userinfo)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(request.FILES, instance=request.user.userprofile)
        context = {
            'user': request.user,
            'u_form': u_form,
            'p_form': p_form,
            'orders': orders,
        }
    return render(request, 'user/profile.html', context)