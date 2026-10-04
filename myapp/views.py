import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import Category, Vegetable, CartItem, Order
from . forms import RegistrationForm, LoginForm

# Create your views here.
def home(request):
    vegetables = Vegetable.objects.all()
    categories = Category.objects.all().order_by('category_name')
    return render(request, 'home.html', {'categories':categories, 'vegetables':vegetables})

def userReg(request):
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your registration is successfulll')
                return redirect('log-page')
            except Exception as e:
                messages.error(request, e)
    else:
        form=RegistrationForm()
    return render(request, 'registration.html', {'form':form})

def userLogin(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-page')

        else:
            messages.error(request, 'Invalid username or password')
            form = LoginForm()

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def userLogout(request):
    logout(request)
    return redirect('log-page')


def add_to_cart(request, id):
	if request.user.is_authenticated:
		product = Vegetable.objects.get(id=id)
		cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
		cart_item.quantity += 1
		cart_item.save()
		return redirect('crt-page')
	else:
		return redirect('/login')
     
def view_cart(request):
	if request.user.is_authenticated:
		cart_items = CartItem.objects.filter(user=request.user)
		total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
		total_price=int(total_price)
		return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
	else:
		return redirect('/login')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated successfully.")
    return redirect('/cart')  # 'cart' is the name of the cart view

@login_required
def delete_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('/cart')


def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100  # Amount in paise
        #print("Request data:", request.POST)
        address=request.POST['address']
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": "user_email@example.com",
            },
        }

        order = client.order.create(data=payment_data)

        # Include key, name, description, and image in the JSON response
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "Vegetables",
            "description": "Payment for Your Order",
            "image": "https://yourwebsite.com/logo.png",  # Replace with your logo URL
        }
        cart_items=CartItem.objects.filter(user=request.user)
        # payment_id=response_data.id
        for cart in cart_items:
            Order.objects.get_or_create(user=request.user, product= cart.product, quantity=cart.quantity, payment_status='success', address=address)

        CartItem.objects.filter(user=request.user).delete()

        return JsonResponse(response_data)
    return redirect('/my_orders')


def payment_success(request):
    return render(request, "payment_success.html")


def my_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by("-date_ordered")
        return render(request, "my_orders.html", {"orders": orders})
    else:
         return redirect('/login')

def shop(request):
    allCategory=Category.objects.all().order_by('category_name')
    allVeg=Vegetable.objects.all()
    return render(request, 'shop.html', {'allVeg':allVeg, 'allCategory':allCategory})

def shopCat(request, id):
    allCategory=Category.objects.all().order_by('category_name')
    allVeg=Vegetable.objects.filter(category_id=id)
    print(allVeg)
    return render(request, 'shop.html', {'allVeg':allVeg, 'allCategory':allCategory})

def contact(request):
     return render(request, 'contact.html')