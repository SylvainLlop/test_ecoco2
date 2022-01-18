from django.core.management.base import BaseCommand
from ecoco2_app.models import CO2rate
from django.utils import timezone
import datetime
import requests


class Command(BaseCommand):
    def handle(self, **options):

        # Récupérer les données de taux de CO2 en France pour les années 2017 et 2018 à partir de l'API décrite ici https://api-recrutement.ecoco2.com/docs/#tag/v1
        current_tz = timezone.get_current_timezone()

        request_params = {'start': '1483225200', 'end': '1546297199'}
        res = requests.get('http://api-recrutement.ecoco2.com/v1/data/', params=request_params)

        input_data = res.json()
        
        # Stocker dans une table django
        for item in input_data:
            date = item['datetime']
            date = timezone.make_aware(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"), current_tz, True)
            rate = item['co2_rate']
 
            if not CO2rate.objects.filter(timestamp=date).exists():
                rate_instance = CO2rate()
                rate_instance.timestamp = date
                rate_instance.co2_rate = rate
                rate_instance.save()
