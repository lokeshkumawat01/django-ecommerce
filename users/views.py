from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .form import CreateUserForm
from .token import account_activation_token 
from orders.models import Address
from orders.form import AddressForm
from .form import LoginForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            #Email verification logic
            subject = 'Verify your email to Activate account'
            message = render_to_string('users/email-verification.html',{
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return redirect('email_verification_sent')

    return render(request, 'users/register.html', {'form': form})

def email_verification(request, uid64, token):
    unique_id = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=unique_id)
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email_verification_success')
    else:
        return redirect('email_verification_failed')

def email_verification_sent(request):
    return render(request, 'users/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'users/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'users/email-verification-failed.html')


def user_login(request):
    form = LoginForm()
    if request.method=='POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')


@login_required

def profile(request):
    # 1. Pehle check karo user ka purana address hai ya nahi
    address_instance = Address.objects.filter(user=request.user).last()

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # address_instance pass karne se ye "Update" karega, None hone par "New Save"
        address_form = AddressForm(request.POST, instance=address_instance)

        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            
            # Address save karte waqt user attach karna zaroori hai
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            
            # Update ke baad wapas profile par hi rakho taaki changes dikhein
            # Aap chaho toh 'index' par bhi bhej sakte ho
            return redirect('profile') 
    else:
        user_form = UserUpdateForm(instance=request.user)
        address_form = AddressForm(instance=address_instance)

    context = {
        'user_form': user_form,
        'address_form': address_form
    }
    return render(request, 'users/profile.html', context)