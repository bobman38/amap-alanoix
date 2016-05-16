from django.core.management.base import BaseCommand, CommandError
from delivery.models import DeliveryDate
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create DeliveryDate for previous & next year'

    def handle(self, *args, **options):
        #today = datetime.combine(date.today(), time.min)
        today = datetime.now() - timedelta(365)
        # get next Tuesday
        days_ahead = 1 - today.weekday() # 1 = Tuesday
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        tuesday = today + timedelta(days_ahead)
        nextyear = datetime.now() + timedelta(365)
        while tuesday < nextyear:
            dates = DeliveryDate.objects.filter(date=tuesday)
            if dates.count()==0:
                date = DeliveryDate()
                date.date = tuesday
                date.save()
            tuesday = tuesday + timedelta(7)
