# inventory/views.py
from django.shortcuts import render, redirect
from .forms import MedicineForm
from django.contrib.auth.decorators import login_required
from .models import Medicine,Transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MedicineForm
from .forms import OrderForm
from .forms import TransactionForm
from .models import Order
import csv
from django.http import HttpResponse
from django.db.models import Q 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils.dateparse import parse_date


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required(login_url='login')
def home(request):
    # Get start and end dates from the request (query parameters)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse the dates (if provided)
    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)

    # Debugging: Print to the console to ensure the dates are being parsed
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")

    # Filter transactions based on date range
    if start_date and end_date:
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])
    elif start_date:
        transactions = Transaction.objects.filter(date__gte=start_date)
    elif end_date:
        transactions = Transaction.objects.filter(date__lte=end_date)
    else:
        transactions = Transaction.objects.all()  # No date filter

    # Income, Expense, and Profit Calculation
    total_income = sum(t.income for t in transactions if t.income is not None)
    total_expense = sum(t.expense for t in transactions if t.expense is not None)
    profit = total_income - total_expense

    context = {
        'orders': Order.objects.all(),
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'profit': profit,
        'start_date': request.GET.get('start_date'),
        'end_date': request.GET.get('end_date'),
    }

    return render(request, 'inventory/home.html', context)


@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = MedicineForm()
    
    return render(request, 'inventory/add_medicine.html', {'form': form})

@login_required
def update_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
        return redirect('inventory')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'inventory/update_medicine.html', {'form': form, 'medicine': medicine})

@login_required
def inventory(request):
    query = request.GET.get('q', '')
    if query:
        medicines = Medicine.objects.filter(name__icontains=query)
    else:
        medicines = Medicine.objects.all()
        
    context = {
        'medicines': medicines
    }
    return render(request, 'inventory/inventory.html', context)
# Delete view
@login_required
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('inventory')
    return render(request, 'inventory/confirm_delete.html', {'medicine': medicine})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            product = order.product
            
            # Check if the quantity exceeds available stock
            if order.quantity > product.quantity:
                messages.error(request, f"Available quantity is only {product.quantity}.")
                return render(request, 'inventory/create_order.html', {'form': form})

            # Update product quantity and save the order
            product.quantity -= order.quantity
            product.save()

            order.total_price = product.Product_price * order.quantity
            order.save()
            messages.success(request, 'Order created successfully!')
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'inventory/create_order.html', {'form': form})

# CREATE
@login_required
def create_transaction(request):
    if request.method == 'POST':
        # Determine which form was submitted (income or expense)
        income = request.POST.get('income')
        expense = request.POST.get('expense')

        # Validate that either income or expense is provided
        if income or expense:
            Transaction.objects.create(
                income=float(income) if income else 0,
                expense=float(expense) if expense else 0,
            )
            return redirect('home')
        else:
            messages.error(request, 'You must enter either income or expense.')

    return render(request, 'inventory/create_transaction.html')

# READ (List all transactions)
@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'inventory/transaction_list.html', {'transactions': transactions})

# UPDATE
@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('home')  # Redirect to transaction list after update
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'inventory/update_transaction.html', {'form': form, 'transaction': transaction})

# DELETE
@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('home')
    return render(request, 'inventory/delete_transaction.html', {'transaction': transaction})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.all()  # Fetch all transactions from the database

    context = {
        'transactions': transactions,
    }

    return render(request, 'inventory/view_transactions.html', context)

@login_required
def recent_orders(request):
    recent_orders = Order.objects.all().order_by('-order_date')[:10]  # Fetch last 10 recent orders
    return render(request, 'inventory/orders.html', {'orders': recent_orders})

@login_required
def search_orders(request):
    query = request.GET.get('q')
    if query:
        orders = Order.objects.filter(
            Q(customer_name__icontains=query) | 
            Q(product__Product_name__icontains=query)  # Use double underscore to access related model's field
        )
    else:
        orders = Order.objects.all()
    
    context = {
        'orders': orders
    }
    return render(request, 'inventory/search_results.html', context)
@login_required
def export_orders_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer Name', 'Product Name', 'Product Price', 'Quantity', 'Total Price', 'Order Date'])

    # Correctly reference the related product fields
    orders = Order.objects.all().values_list('id', 'customer_name', 'product__Product_name', 'product__Product_price', 'quantity', 'total_price', 'order_date')

    for order in orders:
        writer.writerow(order)

    return response

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Fetch the order by ID
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # Prepopulate the form with existing data
        if form.is_valid():
            updated_order = form.save(commit=False)  # Update order instance without saving to database
            updated_order.total_price = updated_order.product.Product_price * updated_order.quantity  # Recalculate total price
            updated_order.save()  # Save the updated order
            return redirect('home')  # Redirect back to home after editing
    else:
        form = OrderForm(instance=order)  # Load the form with current order data

    return render(request, 'inventory/edit_order.html', {'form': form, 'order': order})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()  # Delete the order
        return redirect('home')  # Redirect back to home after deleting

    return render(request, 'inventory/delete_order.html', {'order': order})


