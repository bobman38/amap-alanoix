# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date, datetime, time
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.utils.crypto import get_random_string

from .models import *
from blog.models import Entry
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import FamilyForm

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
    members = Membership.objects.filter(family__profiles__user=request.user, contract__date_max__gte=today_min)
    entries = Entry.objects.order_by('-publication_date')[:5]
    family = None;
    families = Family.objects.filter(profiles__user=request.user)
    if(families.count()>0):
        family = families[0]
    return render(request, 'delivery/home.html',
        {'deliveries' : next_deliveries,
         'contracts' : current_contracts,
         'members' : members,
         'family' : family,
         'perms' : getPerms(family),
         'entries': entries,
        })

@permission_required('delivery.add_order', raise_exception=True)
def manager(request):
    contracts = Contract.objects.all()
    families = Family.objects.filter(leave_date__isnull=True)
    perms = []
    for family in families:
        perms.extend(getPerms(family))

    return render(request, 'delivery/manager.html',
        {'contracts': contracts,
         'perms' : perms,
        })

def getPerms(family):
    year  = datetime.now().year - 2
    perms = []
    if(family != None):
        while year <= datetime.now().year:
            color = 'lightgreen'
            min = 2 * family.ratiohere(year)/365
            if family.countref(year) < min:
                color = 'orange'
            perms.append({"family": family, "year": year, "ratio": family.ratiohere(year), "min": min,  "value": family.countref(year), "color": color})
            year = year + 1
    return perms

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
    families = Family.objects.filter(id__in=Membership.objects.filter(contract=deliverydate.contracts.all).values_list('family_id', flat=True)).order_by('name')
    return render(request, 'delivery/detail.html',
        {'delivery' : deliverydate,
        'families' : families,
        })

@permission_required('delivery.add_order', raise_exception=True)
def contractedit(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    members = Membership.objects.filter(contract=contract).order_by('family__name')
    return render(request, 'delivery/contract_edit.html',
        {'contract' : contract,
        'members' : members,
        })

def contractview(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    members = Membership.objects.filter(contract=contract).order_by('family__name')
    return render(request, 'delivery/contract_view.html',
        {'contract' : contract,
        'members' : members,
        })

@permission_required('delivery.add_order', raise_exception=True)
def contracteditaccount(request, contract_id):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            # Create user + family + profile
            family = Family()
            family.name = form.cleaned_data['name']
            family.save()
            password = get_random_string(length=6)
            user = User.objects.create_user( form.cleaned_data['username'], form.cleaned_data['email'], password)
            profile = Profile()
            profile.family=family
            profile.user=user
            profile.tel = form.cleaned_data['tel']
            profile.save()

            # Send welcome mail
            text = get_template('delivery/mail/newfamily.txt')
            d = Context({ 'user': user, 'password': password, 'url' : settings.URL })
            text_content = text.render(d)
            send_mail('[AMAP a la noix] Compte Utilisateur', text_content, 'no-reply@alanoix.fr', [user.email], fail_silently=False)

            messages.info(request, 'Foyer et utilisateur créé. Un mail a été envoyé à l\'utilisateur avec ses infos de connexion au site.')
        return redirect('delivery:contract_edit_account', contract_id=contract_id)
    else:
        contract = get_object_or_404(Contract, pk=contract_id)
        members = Membership.objects.filter(contract=contract).order_by('family__name')
        families = Family.objects.filter(leave_date__isnull=True).exclude(id__in = Membership.objects.filter(contract=contract).values_list('family_id', flat=True)).order_by('name')
        form = FamilyForm()
        return render(request, 'delivery/contract_edit_account.html',
            {'contract': contract,
            'members': members,
            'families': families,
            'status': Membership.STATUS,
            'form': form,
            })

@permission_required('delivery.add_order', raise_exception=True)
def addfamilytocontract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    member = Membership()
    member.family = get_object_or_404(Family, pk=request.GET.get('family'))
    member.contract = contract
    member.status = 0
    member.save()
    return redirect('delivery:contract_edit_account', contract_id=contract_id)


@permission_required('delivery.add_order', raise_exception=True)
def setorder(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    member = get_object_or_404(Membership, pk=request.POST.get('member'))
    date = get_object_or_404(DeliveryDate, pk=request.POST.get('date'))
    qty = request.POST.get('quantity')

    orders = Order.objects.filter(date=date, member=member, product=product)[:1]
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
            order.member = member
            order.date = date
            order.quantity = qty
            order.save()
    return HttpResponse("OK")

@permission_required('delivery.add_order', raise_exception=True)
def setstatus(request):
    member = get_object_or_404(Membership, pk=request.POST.get('member'))
    status = request.POST.get('status')
    member.status = status
    if member.status>1:
        member.amount = member.computeAmount()
    member.save()
    return HttpResponse("OK")


@login_required
def getorder(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    family = get_object_or_404(Membership, pk=request.POST.get('family'))
    date = get_object_or_404(DeliveryDate, pk=request.POST.get('date'))
    members = Membership.objects.filter(family=family.id)
    orders = Order.objects.filter(date=date, member=members, product=product)[:1]
    if(orders.count()==1):
        order = orders[0]
        return JsonResponse({'qty':order.quantity})
    else:
        return JsonResponse({'qty':None})

@login_required
def getorderalldates(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    member = get_object_or_404(Membership, pk=request.POST.get('member'))
    contract = get_object_or_404(Contract, pk=request.POST.get('contract'))
    orders = Order.objects.filter(date__contracts=contract, member=member, product=product)
    result = []
    for order in orders:
        result.append({"date": order.date.id, "qty": order.quantity})
    return JsonResponse(result, safe=False)

@login_required
def list_users(request):
    profiles = Profile.objects.filter(family__leave_date__isnull=True).order_by('family__name')
    return render(request, 'delivery/list_users.html',
        {'profiles' : profiles})

@login_required
def list_producers(request):
    producers = Producer.objects.all().order_by('name')
    return render(request, 'delivery/list_producers.html',
        {'producers' : producers})
