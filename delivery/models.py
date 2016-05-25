# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from datetime import datetime
from django.db.models.signals import m2m_changed

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    family = models.ForeignKey('Family', blank=True, null=True, related_name="profiles")
    tel = models.CharField(max_length=100, blank=True, null=True)

class Family(models.Model):
    name = models.CharField(max_length=200, unique=True)
    #users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    create_date = models.DateField('Date de Creation',
        default=datetime.now)
    leave_date = models.DateField('Date de départ',
            blank=True,
            null=True)
    def countref(self, year):
        return DeliveryDate.objects.filter(date__year=year, ref_users__profile__family=self).count()
    def ratiohere(self, year):
        start = datetime(year=year, month=1, day=1).date()
        end = datetime(year=year, month=12, day=31).date()
        if self.create_date > end:
            start = end
        elif  self.create_date > start :
            start = self.create_date
        if datetime.now().date() < end :
            end = datetime.now().date()
        delta = end-start
        return float(delta.days)
    def __str__(self):
        return self.name
    def count_users(self):
        return self.profiles.count()

class Producer(models.Model):
    name = models.CharField(max_length=200)
    short_product_name = models.CharField(max_length=5)
    description = models.TextField(blank=True,
        null=True)
    mail = models.EmailField(blank=True,
        null=True)
    tel = models.CharField(max_length=200,
        blank=True,
        null=True)
    address = models.CharField(max_length=500,
        blank=True,
        null=True)
    web = models.URLField(blank=True,
        null=True)
    ref_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.name

class Product(models.Model):
    producer = models.ForeignKey(Producer, related_name="products")
    name = models.CharField(max_length=200)
    unit_price = models.FloatField()
    def get_order(self, family, date):
        members = Membership.objects.filter(family=family.id)
        orders = Order.objects.filter(date=date, member=members, product=self)[:1]
        if(orders.count()==1):
            return str(orders[0])
        else:
            return ""
    def __str__(self):
        return self.name

class DeliveryDate(models.Model):
    date = models.DateField('Date de Livraison', unique=True)
    ref_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True)
    comment = models.CharField(max_length=500,
        blank=True,
        null=True)
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    def count_users(self):
        return self.ref_users.count()
    class Meta:
        ordering = ['date']

class Contract(models.Model):
    producer = models.ForeignKey(Producer)
    name = models.CharField(max_length=200)
    dates = models.ManyToManyField(DeliveryDate, related_name="contracts")
    date_min = models.DateField(null=True)
    date_max = models.DateField(null=True)
    members = models.ManyToManyField(Family, through="Membership")
    def __str__(self):
        return self.name
    def count_dates(self):
        return self.dates.count()

class Membership(models.Model):
    family = models.ForeignKey(Family)
    contract = models.ForeignKey(Contract)
    status = models.IntegerField()
    comment = models.CharField(max_length=500, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    class Meta:
        unique_together = ('family', 'contract')
    def __str__(self):
        return self.family.name
    STATUS = {0:'EN ATTENTE', 1:'CONTRAT OK', 2:'CHEQUE OK', 3:'CONT/CHEQ OK', 4:'TRANSMIS PROD', 5:'PROBLEME'}
    COLOR = {0:'#F5D0A9', 1:'#F5D0A9', 2:'#F5D0A9', 3:'lightgreen', 4:'lightgreen', 5:'#F78181'}
    def statusName(self):
        return self.STATUS[self.status]
    def statusColor(self):
        return self.COLOR[self.status]
    def computeAmount(self):
        total_price = 0
        orders = Order.objects.filter(member=self, product__producer=self.contract.producer, date__contracts=self.contract)
        for order in orders:
            total_price = total_price + order.price()
        return total_price

class Order(models.Model):
    member = models.ForeignKey(Membership, related_name="orders")
    product = models.ForeignKey(Product)
    date = models.ForeignKey(DeliveryDate)
    quantity = models.FloatField()
    def __str__(self):
        return str(self.quantity)
    def price(self):
        return self.quantity*self.product.unit_price
    class Meta:
        unique_together = ('member', 'product', 'date')

def update_contract_dates(sender, instance, action, reverse, **kwargs):
    if(instance.dates.count()>0):
        instance.date_min = None
        instance.date_max = None
        for date in instance.dates.all():
            if instance.date_min is None or instance.date_min > date.date:
                instance.date_min = date.date
            if instance.date_max is None or instance.date_max < date.date:
                instance.date_max = date.date
        instance.save()

m2m_changed.connect(update_contract_dates, sender=Contract.dates.through, dispatch_uid="update_contract_dates")
