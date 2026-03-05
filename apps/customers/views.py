import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CSVImportForm, CustomerForm
from .models import Customer


@login_required
def customer_list(request):
    customers = Customer.objects.filter(owner=request.user)
    q = request.GET.get('q', '').strip()
    if q:
        customers = customers.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
            | Q(company__icontains=q)
        )
    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'search_query': q,
    })


@login_required
def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.owner = request.user
            customer.save()
            messages.success(request, 'Customer added.')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': 'Add Customer',
    })


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated.')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': 'Edit Customer',
    })


@login_required
def customer_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    customer = get_object_or_404(Customer, pk=pk, owner=request.user)
    customer.delete()
    messages.success(request, 'Customer deleted.')
    return redirect('customers:customer_list')


@login_required
def customer_import(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded = csv_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            success_count = 0
            error_count = 0
            for row in reader:
                first_name = row.get('first_name', '').strip()
                last_name = row.get('last_name', '').strip()
                if not first_name or not last_name:
                    error_count += 1
                    continue
                Customer.objects.create(
                    owner=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    email=row.get('email', '').strip(),
                    company=row.get('company', '').strip(),
                )
                success_count += 1
            messages.success(
                request,
                f'Imported {success_count} customers. {error_count} rows skipped.',
            )
            return redirect('customers:customer_list')
    else:
        form = CSVImportForm()
    return render(request, 'customers/customer_import.html', {'form': form})


@login_required
def customer_search_api(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 1:
        return JsonResponse([], safe=False)
    customers = Customer.objects.filter(
        owner=request.user,
    ).filter(
        Q(first_name__icontains=q)
        | Q(last_name__icontains=q)
        | Q(email__icontains=q)
        | Q(company__icontains=q)
    )[:10]
    results = [
        {
            'id': c.id,
            'name': str(c),
            'company': c.company,
        }
        for c in customers
    ]
    return JsonResponse(results, safe=False)
