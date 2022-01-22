from sqlite3 import Timestamp
from django.core.management.base import BaseCommand
from ecoco2_app.models import CO2rate, LowFrequencyCO2rate

from django.utils import timezone

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Command(BaseCommand):
    def handle(self, **options):

        current_tz = timezone.get_current_timezone()
        date_from = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=current_tz)
        date_to = datetime.datetime(2018, 1, 7, 23, 59, 59, tzinfo=current_tz)

        # df_init = pd.DataFrame(list(CO2rate.objects.all().values()))
        df_init = pd.DataFrame(list(CO2rate.objects.filter(timestamp__gte=date_from, timestamp__lte=date_to).values()))
        df_init = df_init[['timestamp', 'co2_rate']].set_index('timestamp')

        # Filtrer les données pour produire une deuxième table avec une fréquence horaire
        df_filtered = df_init.resample('2H').ffill()
        df_filtered.reset_index(inplace=True)

        df_records = df_filtered.to_dict('records')

        model_instances = [LowFrequencyCO2rate(
            timestamp=record['timestamp'],
            co2_rate=record['co2_rate'],
        ) for record in df_records]

        LowFrequencyCO2rate.objects.bulk_create(model_instances)

        
