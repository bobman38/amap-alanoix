from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date, datetime, time
from django.http import HttpResponse, JsonResponse

from .models import DeliveryDate, Contract, Order, Family, Product

def index(request):
    return render(request, 'delivery/start.html',
        {})

def error403(request):
    return render(request, 'delivery/error/403.html')

def error404(request):
    return render(request, 'delivery/error/404.html')

@login_required
def home(request):
    today_min = datetime.combine(date.today(), time.min)
    next_deliveries = DeliveryDate.objects.filter(date__gte=today_min).order_by('date')[:5]
    current_contracts = Contract.objects.filter(date_max__gte=today_min)
    return render(request, 'delivery/home.html',
        {'deliveries' : next_deliveries,
         'contracts' : current_contracts,
        })

@login_required
def addme(request, deliverydate_id):
    deliverydate = get_object_or_404(DeliveryDate, pk=deliverydate_id)
    deliverydate.ref_users.add(request.user)
    deliverydate.save()
    return redirect('delivery:home')

@login_required
def removeme(request, deliverydate_id):
    deliverydate = get_object_or_404(DeliveryDate, pk=deliverydate_id)
    deliverydate.ref_users.remove(request.user)
    deliverydate.save()
    return redirect('delivery:home')

@login_required
def detail(request, deliverydate_id):
    deliverydate = get_object_or_404(DeliveryDate, pk=deliverydate_id)
    families = Family.objects.filter(leave_date__isnull=True).order_by('name')
    return render(request, 'delivery/detail.html',
        {'delivery' : deliverydate,
        'families' : families,
        })

@permission_required('delivery.can_manage', raise_exception=True)
def manage(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    families = Family.objects.filter(leave_date__isnull=True).order_by('name')
    return render(request, 'delivery/manage.html',
        {'contract' : contract,
        'families' : families,
        })

@permission_required('delivery.can_manage', raise_exception=True)
def manageaccount(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    families = Family.objects.filter(leave_date__isnull=True).order_by('name')
    data = []
    for family in families:
        total_price = 0
        orders = Order.objects.filter(family=family, product__producer=contract.producer, date__contracts=contract)
        for order in orders:
            total_price = total_price + order.price()
        data.append({'family': family, 'amount': total_price, 'status': 'ko'})

    return render(request, 'delivery/manageaccount.html',
        {'contract' : contract,
        'data' : data,
        })

@permission_required('delivery.can_manage', raise_exception=True)
def setorder(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    family = get_object_or_404(Family, pk=request.POST.get('family'))
    date = get_object_or_404(DeliveryDate, pk=request.POST.get('date'))
    qty = request.POST.get('quantity')

    orders = Order.objects.filter(date=date, family=family, product=product)[:1]
    if(orders.count()==1):
        order = orders[0]
        if(qty==None or qty=='0' or qty==''):
            order.delete()
        else:
            order.quantity = qty
            order.save()
    else:
        if(not(qty==None or qty==0)):
            order = Order()
            order.product = product
            order.family = family
            order.date = date
            order.quantity = qty
            order.save()
    return HttpResponse("OK")

@login_required
def getorder(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    family = get_object_or_404(Family, pk=request.POST.get('family'))
    date = get_object_or_404(DeliveryDate, pk=request.POST.get('date'))

    orders = Order.objects.filter(date=date, family=family, product=product)[:1]
    if(orders.count()==1):
        order = orders[0]
        return JsonResponse({'qty':order.quantity})
    else:
        return JsonResponse({'qty':None})

@permission_required('delivery.can_manage', raise_exception=True)
def getorderalldates(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    family = get_object_or_404(Family, pk=request.POST.get('family'))
    contract = get_object_or_404(Contract, pk=request.POST.get('contract'))
    orders = Order.objects.filter(date__contracts=contract, family=family, product=product)
    result = []
    for order in orders:
        result.append({"date": order.date.id, "qty": order.quantity})
    return JsonResponse(result, safe=False)
