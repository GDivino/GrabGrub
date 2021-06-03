from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, Food, Customer, Account
from datetime import datetime
import os

# Login/Sign up
def signup(request):
    # Indicator if the user signed up or not
    global signup

    if request.method == 'POST':
        us = request.POST.get('uname')
        pw = request.POST.get('pw')
        if Account.objects.filter(username=us).exists()==True:
            messages.error(request, "User already exists")
            return redirect('log_in')
        else:
            Account.objects.create(username=us, password=pw)
            signup = True # Set Sign up indicator to true
            messages.success(request, "Account created successfully :D")
            return redirect('log_in')
    return render(request, 'Kiosk/signup.html')

def log_in(request):
    # Indicator for log in
    global is_loggedin

    # Checks if sign up was successful
    exists = "signup_success" in globals()
    if exists == True:
        if signup_success == True:
            # Get list of globals
            globals_list = globals()
            messages.success(request, "Account Created Successfully")
            
            # Change signup_success variable to false after message was created to allow more signups
            globals_list['signup_success'] = False

    if request.method == 'POST':
        us = request.POST.get('user')
        pw = request.POST.get('pw')
        if Account.objects.filter(username=us, password=pw).exists()== True:
            # Set indicator to true if user was able to log in
            is_loggedin = True
            return redirect('view_order')
        else:
            messages.error(request, 'Invalid username/password.')
    return render(request, 'Kiosk/log_in.html')


# Order/Transactions
def view_order(request):
    exists = "is_loggedin" in globals() # Looks for indicator in the global space
    auth = False # Authentication check

    # Sets authentication check to true if user successfully logged in
    if exists == True:
        if is_loggedin == True:
            auth = True

    if auth == True:
        order_list = Order.objects.all()
        return render(request, "Kiosk/orders.html", {"orders": order_list})
    else: 
        return redirect("log_in")

def view_order_detail(request, pk):
    order_details = get_object_or_404(Order, pk=pk)
    return render(request, "Kiosk/order_details.html", {"o": order_details})

def add_order(request):
    exists = "is_loggedin" in globals() # Looks for indicator in the global space
    auth = False # Authentication check

    # Sets authentication check to true if user successfully logged in
    if exists == True:
        if is_loggedin == True:
            auth = True

    if auth == True:
        if request.method == "POST":
            food_pk = request.POST.get("food")
            qty = request.POST.get("qty")
            date = request.POST.get("date")
            cust_pk = request.POST.get("cust")
            mode = request.POST.get("mode")

            food = Food.objects.get(pk=food_pk)
            cust = Customer.objects.get(pk=cust_pk)

            if date == "":
                date = datetime.now()

            # If order already exists
            if Order.objects.filter(food=food, ordered_at=date, cust_order=cust, payment_mode=mode, qty=qty).exists() == True:
                messages.error(request, "Order already exists")
                cust_choices = Customer.objects.all()
                food_choices = Food.objects.all()
                return render(request, "Kiosk/add_order.html", {"customers":cust_choices, "food":food_choices})
            
            # If order is added successfully
            else:
                Order.objects.create(food=food, ordered_at=date, cust_order=cust, payment_mode=mode, qty=qty)
                messages.success(request, "Successfully added order")
                cust_choices = Customer.objects.all()
                food_choices = Food.objects.all()
                return render(request, "Kiosk/add_order.html", {"customers":cust_choices, "food":food_choices})
        else:
            cust_choices = Customer.objects.all()
            food_choices = Food.objects.all()
            return render(request, "Kiosk/add_order.html", {"customers":cust_choices, "food":food_choices})
    else:
        return redirect("log_in")
            
def update_order(request, pk):
    if request.method == "POST":
        qty = request.POST.get("qty")
        mode = request.POST.get("mode")
        
        Order.objects.filter(pk=pk).update(payment_mode=mode, qty=qty)
        messages.success(request, "Order updated successfully")
        return redirect("view_order")
    else:
        order_details = get_object_or_404(Order, pk=pk)
        return render(request, "Kiosk/update_order.html", {"o":order_details})

def delete_order(request, pk):
    Order.objects.filter(pk=pk).delete()
    messages.success(request, "Order cancelled")
    return redirect("view_order")


# Food items
def view_food(request):
    exists = "is_loggedin" in globals() # Looks for indicator in the global space
    auth = False # Authentication check

    # Sets authentication check to true if user successfully logged in
    if exists == True:
        if is_loggedin == True:
            auth = True

    if auth == True:
        food_page = Food.objects.all()
        return render(request, "Kiosk/food.html", {"food":food_page})
    else:
        return redirect("log_in")

def add_food(request):
    exists = "is_loggedin" in globals() # Looks for indicator in the global space
    auth = False # Authentication check

    # Sets authentication check to true if user successfully logged in
    if exists == True:
        if is_loggedin == True:
            auth = True

    if auth == True:
        if(request.method=="POST"):
            foodname = request.POST.get('foodname')
            fooddescription = request.POST.get('fooddescription')
            foodprice = request.POST.get('foodprice')
            foodcreated = request.POST.get('foodcreated')

            # Get Image upload
            files = request.FILES.get("image")

            if Food.objects.filter(name = foodname).exists() == True:
                messages.error(request, 'Food Item Already Exists.')
                return render(request, 'Kiosk/add_food.html')
            else:
                Food.objects.create(name=foodname, description=fooddescription, price=foodprice, created_at=foodcreated, image=files)
                messages.success(request, "Food Item Added")
                return redirect('view_food')
        return render(request, 'Kiosk/add_food.html')
    else:
        return redirect("log_in")

def view_food_details(request, pk):
    f = get_object_or_404(Food, pk=pk)
    return render(request, "Kiosk/fooddetails.html", {"f":f})

def update_food_details(request, pk):
    if request.method=="POST":
        foodname = request.POST.get('foodname')
        fooddescription = request.POST.get('fooddescription')
        foodprice = request.POST.get('foodprice')
        foodcreated = request.POST.get('foodcreated')
        files = request.FILES.get("image")

        food = get_object_or_404(Food, pk=pk)
        if files == None:
            files = food.image
        else:
            if food.image:
                os.remove(food.image.path)
            food_details = Food.objects.get(pk=pk)
            food_details.image = files
            food_details.save()

        # If no date is inputted
        if foodcreated == "":
            x = get_object_or_404(Food, pk=pk)
            foodcreated = x.created_at

        if Food.objects.exclude(name=food.name).filter(name = foodname).exists() == True:
            messages.error(request, 'Food Item Already Exists.')
            f = get_object_or_404(Food, pk=pk)
            return render(request, 'Kiosk/update_food_details.html', {"f":f})
        else:
            Food.objects.filter(pk=pk).update(name=foodname, description=fooddescription, price=foodprice, created_at=foodcreated)
            messages.success(request, 'Details Updated')
            return redirect('update_food_details', pk=pk)
    else:
        f = get_object_or_404(Food, pk=pk)
        return render(request, "Kiosk/update_food_details.html", {"f":f})

def delete_food(request, pk):
    food_details = get_object_or_404(Food, pk=pk)

    # Delete image in directory
    if food_details.image:
        food_img = food_details.image.path
        if os.path.exists(food_img):
            os.remove(food_img)

    Food.objects.filter(pk=pk).delete()
    messages.success(request, 'Food Item Deleted')
    return redirect('view_food')


# Customers
def view_customer(request):
    exists = "is_loggedin" in globals() # Looks for indicator in the global space
    auth = False # Authentication check

    # Sets authentication check to true if user successfully logged in
    if exists == True:
        if is_loggedin == True:
            auth = True

    if auth == True:
        customer_page = Customer.objects.all()
        return render(request, "Kiosk/customer.html", {"customer":customer_page})
    else:
        return redirect("log_in")

def add_customer(request):
    exists = "is_loggedin" in globals() # Looks for indicator in the global space
    auth = False # Authentication check

    # Sets authentication check to true if user successfully logged in
    if exists == True:
        if is_loggedin == True:
            auth = True
    
    if auth == True:
        if(request.method=="POST"):
            name = request.POST.get('name')
            address = request.POST.get('address')
            city = request.POST.get('city')
            created = request.POST.get('created')

            files = request.FILES.get("image")

            if Customer.objects.filter(name = name).exists() == True:
                messages.error(request, 'Customer Already Exists.')
                return render(request, 'Kiosk/add_customer.html')
            else:
                Customer.objects.create(name=name, address=address, city=city, created_at=created, image=files)
                messages.success(request, "Customer Added")
                return redirect('view_customer')
        return render(request, 'Kiosk/add_customer.html')
    else:
        return redirect("log_in")

def view_customer_details(request, pk):
    f = get_object_or_404(Customer, pk=pk)
    return render(request, "Kiosk/customerdetails.html", {"f":f})

def update_customer_details(request, pk):
    if(request.method=="POST"):
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        date = request.POST.get("date")
        files = request.FILES.get("image")

        customer = get_object_or_404(Customer, pk=pk)
        if files == None:
            files = customer.image
        else:
            if customer.image:
                os.remove(customer.image.path)
            cust_details = Customer.objects.get(pk=pk)
            cust_details.image = files
            cust_details.save()

        # If no date is supplied
        if date == "":
            x = get_object_or_404(Customer, pk=pk)
            date = x.created_at

        if Customer.objects.exclude(name=customer.name).filter(name = name).exists() == True:
            messages.error(request, 'Customer Already Exists.')
            c = get_object_or_404(Customer, pk=pk)
            return render(request, "Kiosk/update_customer_details.html", {"f":c})
        else:
            Customer.objects.filter(pk=pk).update(name=name, address=address, city=city, created_at=date)
            messages.success(request, 'Customer Details Updated')
            c = get_object_or_404(Customer, pk=pk)
            return render(request, "Kiosk/update_customer_details.html", {"f":c})
    else:
        c = get_object_or_404(Customer, pk=pk)
        return render(request, "Kiosk/update_customer_details.html", {"f":c})

def delete_customer(request, pk):
    cust_details = get_object_or_404(Customer, pk=pk)

    # Delete image in directory
    if cust_details.image:
        cust_img = cust_details.image.path
        if os.path.exists(cust_img):
            os.remove(cust_img)

    Customer.objects.filter(pk=pk).delete()
    messages.success(request, 'Customer Information Deleted')
    return redirect('view_customer')