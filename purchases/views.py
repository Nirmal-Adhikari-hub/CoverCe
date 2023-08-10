import random
import stripe
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from products.models import Product
from .models import Purchase

from cfehome.env import config 



BASE_ENDPOINT = "http://127.0.0.1:8000"
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY
# Create your views here.


def register_with_logout_view(request):
    if request.method == 'POST':
        if request.POST.get('logout'):
            logout(request)
            return redirect('register')  # Redirect to the registration form

    return render(request, 'registration/confirm_logout.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('register_with_logout')  # Log out the user if they're already authenticated

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, 'Registration unsuccessful.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)            
            # Get the 'next' parameter from the request
            next_url = request.POST.get('next')
            if next_url:
                messages.success(request, "Logged in successfully!")
                return redirect(next_url)
            else:
                messages.success(request, "Logged in successfully!")
                return redirect('home')  # Redirect to a default URL if 'next' is not provided
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'registration/login.html')  

@login_required
def logout_view(request):
    next_url = request.GET.get('next', None)  # Get the 'next' parameter from the URL

    logout(request)
    messages.info(request, 'You have been logged out successfully.')

    if next_url:
        return redirect(next_url)  # Redirect to the stored URL
    else:
        return redirect('home')  # Redirect to a default page if 'next' parameter is not provided

@login_required
def user_surprise(request):
    return render(request, 'registration/surprise.html')


# @login_required
def purchase_start_view(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        messages.info(request, 'Please, login to continue the purchase.')
        return redirect('login')
    handle = request.POST.get("handle")
    obj = Product.objects.get(handle=handle)
    stripe_price_id = obj.stripe_price_id
    if stripe_price_id is None:
        return HttpResponseBadRequest()
    purchase = Purchase.objects.create(user=request.user, product=obj)
    request.session['purchase_id'] = purchase.id
    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    cancel_path = reverse("purchases:stopped")
    success_url = f"{BASE_ENDPOINT}{success_path}"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}"
    print(success_url, cancel_url)
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()
    # number = random.randint(0, 1)
    # print(number)
    # if number == 1:
    #     return HttpResponseRedirect('/purchases/success')
    # # strip api
    return HttpResponseRedirect(checkout_session.url)
    # return HttpResponse('Started')


@login_required
def purchase_success_view(request):
    purchase_id = request.session.get('purchase_id')
    if purchase_id:  
      purchase = Purchase.objects.get(id=purchase_id)
      purchase.is_completed = True
      purchase.save()
      del request.session['purchase_id']
      return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse(f"Finished {  purchase_id }")


@login_required
def purchase_stopped_view(request):
    purchase_id = request.session.get('purchase_id')
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        product = purchase.product
        return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponse('Stopped')
