from django.core.management.base import BaseCommand, CommandError
from delivery.models import DeliveryDate
from django.contrib.auth.models import User
from datetime import date, datetime, time
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mass_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Check if next delivery have at least 1 ref user'

    def handle(self, *args, **options):
        today_min = datetime.combine(date.today(), time.min)
        delivery = DeliveryDate.objects.filter(date__gte=today_min).order_by('date')[:1][0]
        if(delivery.count_users()==0):
            text = get_template('delivery/mail/checkdelivery.txt')
            d = Context({ 'delivery': delivery, 'url' : settings.URL })
            text_content = text.render(d)
            users = User.objects.filter(is_active=True, family__leave_date__isnull=True).exclude(email='')
            tuple = ()
            for user in users:
                tuple = tuple + ((
                    '[AMAP a la noix] Besoin de perm !',
                    text_content,
                    'no-reply@alanoix.fr',
                    [user.email, ]),)
            print (tuple)
            send_mass_mail(tuple)
