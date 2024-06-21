from django.shortcuts import render, redirect
from . models import *
from django.http import HttpResponse
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .forms import OrderForm
from.models import *
from .models import Order, OrderItem
from .forms import OrderForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.template.loader import get_template
from django.template import Context
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from .generateAccesstoken import get_access_token
from .stkPush import initiate_stk_push
from .query import query_stk_status 
from django_daraja.mpesa.core import MpesaClient

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Customer

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

  # Import the module required to create pdf documents from html

from .models import Customer



def index(request):
    cl = MpesaClient()
    phone_number = '254114232496'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference,transaction_desc, callback_url)

    return HttpResponse(response)



def ripota(request):
    # Get products from the database
    products = Product.objects.all()
    logo = Logo.objects.first()

    # Render the product report template with product data
    template = get_template('store/product_report.html')
    html = template.render({'products': products, 'logo': logo})

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="ripotaa.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
    if pisa_status.err:
        return HttpResponse('Failed to generate PDF', status=500)

    return response


def ripota1(request):
    # Get products from the database
    products = Product.objects.all()
    logo = Logo.objects.first()
    

    # Render the product report template with product data
   
    context={'products': products, 'logo':logo}


    return render(request, 'store/ripota1.html', context)

    
    






def generate_pdf_report(request):
    customers = Customer.objects.all()
    logo = Logo.objects.first()

    template_path = 'store/customer_report.html'
    context = {'customers': customers, 'logo':logo}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="customer_report.pdf"'

    # Render the template to a html string
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF document
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # If the PDF document is created successfully, return the response
    if pisa_status.err:
        return HttpResponse('Failed to generate PDF')

    return response



def UserPage(request):
    context = {}
    return render(request, 'store/user.html', context)

@never_cache
def search(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
   

    if request.method=='POST':
        searched = request.POST['searched']

        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.error(request, "That product does not exist...Please try again")
            return render(request, 'store/search.html', {})
        else:
            return render(request, 'store/search.html', {'searched': searched, 'products':products, 'cartItems': cartItems})
    else:
        return render(request, 'store/search.html', {})

@login_required(login_url='login')
@admin_only
@never_cache
def home(request):
    #product = get_object_or_404(Product, pk=product_id)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    orders=Order.objects.all()
    customers=Customer.objects.all()

    orders = Order.objects.prefetch_related('orderitem_set__product').all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context={
        'cartItems': cartItems,
        #'product': product,
        'order': order,
        'items': items,
        'orders':orders, 
        'customers':customers, 
        'total_orders':total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'store/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@never_cache
def products(request):

    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context= {
        'products': products,
        'cartItems': cartItems

    }
    
    return render(request, 'store/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    
    products = Product.objects.all()
    order_count = orders.count()

    # Get the selected product ID from the request
    selected_product_id = request.GET.get('product')
    print("Selected Product ID:", selected_product_id)  # Add this line for debugging

   # If a product is selected, filter orders based on the selected product
    if selected_product_id:
        orders = orders.filter(orderitem__product_id=selected_product_id)
        print("Filtered Orders:", orders)  # Debug print
        #print("hapa:", order_item.product.name)
    data = cartData(request)
    cartItems = data['cartItems']
    

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
  

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter, 'products': products, 'cartItems': cartItems, 'selected_product_id': selected_product_id}
    return render(request, 'store/customer.html', context)

    

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Split product description into lines
    description_lines = product.description.split('\n')

    context = {
        'cartItems': cartItems,
        'product': product,
        'order': order,
        'items': items,
        'description_lines': description_lines,  # Pass the description lines to the template
    }

    return render(request, 'store/detail.html', context)



@login_required(login_url='login')
@never_cache
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    

    
    products = Product.objects.all()
    context={'products':products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

@login_required(login_url='login')
@never_cache
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items ,'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
@never_cache
def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items ,'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id= productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1) 

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total ==float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)

@unauthenticated_user
def registerPage(request):    
    form = CreateUserForm()
    context = {}
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        phone = request.POST.get('phone')
        if form.is_valid():
            user = form.save()
            customer, created = Customer.objects.get_or_create(user=user)
            customer.phone = phone
            customer.save()
            
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request,'Account was created for' + username)

            return redirect('login')

    
    context['form']= form
    return render(request, 'store/register.html', context)


@unauthenticated_user
def loginPage(request):
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'store/login.html', context)
            
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    products = Product.objects.all()  # Retrieve all products
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()  # Save the order first
            for product_id in request.POST.getlist('products'):  # Retrieve selected product IDs from form
                product = Product.objects.get(pk=product_id)  # Get product instance
                OrderItem.objects.create(order=order, product=product)  # Create OrderItem for each selected product
            return redirect('/')
    context = {'form': form, 'products': products, 'customer':customer}  # Pass products to the template context
    return render(request, 'store/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    products = Product.objects.all()  # Retrieve all products
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()  # Save the updated order first
            order.orderitem_set.all().delete()  # Delete existing order items
            for product_id in request.POST.getlist('products'):  # Retrieve selected product IDs from form
                product = Product.objects.get(pk=product_id)  # Get product instance
                OrderItem.objects.create(order=order, product=product)  # Create OrderItem for each selected product
            return redirect('/')
    context = {'form': form, 'products': products, 'order': order}  # Pass products and order to the template context
    return render(request, 'store/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method =='POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'store/delete.html', context)



def updateOrder1(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    products = Product.objects.all()  # Retrieve all products
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()  # Save the updated order first
            order.orderitem_set.all().delete()  # Delete existing order items
            for product_id in request.POST.getlist('products'):  # Retrieve selected product IDs from form
                product = Product.objects.get(pk=product_id)  # Get product instance
                OrderItem.objects.create(order=order, product=product)  # Create OrderItem for each selected product
            return redirect(reverse('customer', kwargs={'pk': order.customer.pk}))
    context = {'form': form, 'products': products, 'order': order}  # Pass products and order to the template context
    return render(request, 'store/order_form.html', context)

def deleteOrder1(request, order_id, order_item_id):
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.get(id=order_item_id)
    
    if request.method == 'POST':
        order_item.delete()
        return redirect(reverse('customer', kwargs={'pk': order.customer.pk}))
    
    context = {'order_item': order_item, 'order':order}
    return render(request, 'store/delete1.html', context)
