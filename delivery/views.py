# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from datetime import date, datetime, time
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.utils.crypto import get_random_string
from django.utils.html import escape
from django.core.exceptions import PermissionDenied

from .models import *
from blog.models import Entry
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import FamilyForm

import logging
logger = logging.getLogger(__name__)

def is_ref_user(user):
    producers = Producer.objects.all()
    for producer in producers:
        if producer.ref_user == user:
            return True
    if user.is_superuser:
        return True
    return False

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

@user_passes_test(is_ref_user)
def manager(request):
    contracts = Contract.objects.all()
    families = Family.objects.filter(leave_date__isnull=True)
    perms = []
    for family in families:
        perms.extend(getPerms(family, True))

    return render(request, 'delivery/manager.html',
        {'contracts': contracts,
         'perms' : perms,
         'families' : families,
        })

def getPerms(family, onlylate = False):
    year  = datetime.now().year - 2
    perms = []
    if(family != None):
        while year <= datetime.now().year:
            color = 'lightgreen'
            min = 2 * family.ratiohere(year)/365
            if family.countref(year) < min:
                color = 'orange'
            if color == 'orange' or onlylate == False:
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

def detail(request, deliverydate_id):
    deliverydate = get_object_or_404(DeliveryDate, pk=deliverydate_id)
    #families = Family.objects.filter(id__in=Membership.objects.filter(contract=deliverydate.contracts.all).values_list('family_id', flat=True)).order_by('name')
    #members = Membership.objects.filter(contract__dates=deliverydate)
    #contracts = Contract.objects.filter(dates=deliverydate)
    families = Family.objects.filter(id__in=Membership.objects.filter(contract__dates=deliverydate).values_list('family_id', flat=True)).order_by('name')
    return render(request, 'delivery/detail.html',
        {'delivery' : deliverydate,
        'families' : families,
        })

def contractview(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    members = Membership.objects.filter(contract=contract).order_by('family__name')
    return render(request, 'delivery/contract_view.html',
        {'contract' : contract,
        'members' : members,
        })

def contractviewnext(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    today_min = datetime.combine(date.today(), time.min)
    next_deliveries = DeliveryDate.objects.filter(contracts=contract, date__gte=today_min).order_by('date')[:1]

    members = Membership.objects.filter(contract=contract).order_by('family__name')
    return render(request, 'delivery/contract_view_next.html',
        {'contract' : contract,
        'deliveries' : next_deliveries,
        })

def contractedit(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    members = Membership.objects.filter(contract=contract).order_by('family__name')
    if(request.user.is_superuser or contract.producer.ref_user==request.user):
        return render(request, 'delivery/contract_edit.html',
            {'contract' : contract,
            'members' : members,
            })
    else:
        raise PermissionDenied

def contracteditaccount(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if(request.user.is_superuser or contract.producer.ref_user==request.user):
        if request.method == 'POST':
            form = FamilyForm(request.POST)
        else:
            form = FamilyForm()
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
            if form.cleaned_data['send_mail']:
                text = get_template('delivery/mail/newfamily.txt')
                d = Context({ 'user': user, 'password': password, 'url' : settings.URL })
                text_content = text.render(d)
                send_mail('[AMAP a la noix] Compte Utilisateur', text_content, 'no-reply@alanoix.fr', [user.email], fail_silently=False)
                messages.info(request, 'Foyer et utilisateur créé. Un mail a été envoyé à l\'utilisateur avec ses infos de connexion au site.')
            else:
                messages.info(request, 'Foyer et utilisateur créé. Pas d\'email envoyé.')
            return redirect('delivery:contract_edit_account', contract_id=contract_id)
        else:
            members = Membership.objects.filter(contract=contract).order_by('family__name')
            families = Family.objects.filter(leave_date__isnull=True).exclude(id__in = Membership.objects.filter(contract=contract).values_list('family_id', flat=True)).order_by('name')


            # add Price for each Product / Delivery Date for current contrat if not existing !
            # set with the Product.unit_value = default_value
            for product in contract.producer.products.all():
                for deliverydate in contract.dates.all() :
                    prices = Price.objects.filter(deliverydate=deliverydate, product=product)[:1]
                    if(prices.count()==0):
                        price = Price()
                        price.product = product
                        price.deliverydate = deliverydate
                        price.value = product.unit_price
                        price.save()

            return render(request, 'delivery/contract_edit_account.html',
                {'contract': contract,
                'members': members,
                'families': families,
                'status': Membership.STATUS,
                'form': form,
                })
    else:
        raise PermissionDenied

def addfamilytocontract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if(request.user.is_superuser or contract.producer.ref_user==request.user):
        member = Membership()
        member.family = get_object_or_404(Family, pk=request.GET.get('family'))
        member.contract = contract
        member.status = 0
        member.save()
        return redirect('delivery:contract_edit_account', contract_id=contract_id)
    else:
        raise PermissionDenied

def setorder(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    if(request.user.is_superuser or product.producer.ref_user==request.user):
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
    else:
        raise PermissionDenied

def setmembershipinfo(request):
    member = get_object_or_404(Membership, pk=request.POST.get('member'))
    if(request.user.is_superuser or member.contract.producer.ref_user==request.user):
        member.status = request.POST.get('status')
        if(request.POST.get('amount') != None and request.POST.get('amount') != ""):
            member.amount = request.POST.get('amount').replace(',','.')
        else:
            member.amount = None
        member.comment = request.POST.get('comment')
        member.save()
        return HttpResponse("OK")
    else:
        raise PermissionDenied

def setprice(request):
    product = get_object_or_404(Product, pk=request.POST.get('product'))
    if(request.user.is_superuser or product.producer.ref_user==request.user):
        date = get_object_or_404(DeliveryDate, pk=request.POST.get('date'))
        price = Price.objects.filter(deliverydate=date, product=product)[:1][0]
        if(request.POST.get('amount') != ""):
            price.value = request.POST.get('value').replace(',','.')
        else:
            price.value = 0
        price.save()
        return HttpResponse("OK")
    else:
        raise PermissionDenied

@login_required
def list_users(request):
    profiles = Profile.objects.filter(family__leave_date__isnull=True).order_by('family__name')
    families = Family.objects.filter(leave_date__isnull=True)
    return render(request, 'delivery/list_users.html',
        {'profiles' : profiles,
         'families' : families})

@login_required
def list_producers(request):
    producers = Producer.objects.all().order_by('name')
    return render(request, 'delivery/list_producers.html',
        {'producers' : producers})
