from django.core.management.base import BaseCommand
from ecoco2_app.models import CO2rate

from django.utils import timezone

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Command(BaseCommand):
    def handle(self, **options):

        current_tz = timezone.get_current_timezone()
        date_from = datetime.datetime(2015, 12, 31, 0, 0, 0, tzinfo=current_tz)
        date_to = datetime.datetime(2016, 1, 7, 23, 59, 59, tzinfo=current_tz)

        # df_init = pd.DataFrame(list(CO2rate.objects.all().values()))
        df_init = pd.DataFrame(list(CO2rate.objects.filter(timestamp__gte=date_from, timestamp__lte=date_to).values()))
        df_init = df_init[['timestamp', 'co2_rate']].set_index('timestamp')

        # Filtrer les données pour produire une deuxième table avec une fréquence horaire
        df_filtered = df_init.resample('2H').ffill()
        # print(df_filtered)

        # À partir de la table horaire, interpoler les résultats pour (re)obtenir la même fréquence initiale de 30 minutes
        df_reinterpolated = df_filtered.resample('30min').interpolate().bfill()
        # print(df_reinterpolated)
 
        # Afficher les 20 derniers points dans un tableau avec la différence entre la vraie donnée et la donnée interpolée
        df_merged = pd.merge(df_init, df_reinterpolated, how='left', on='timestamp', suffixes=('_init', '_interpolated'))
        df_merged['co2_rate_interpolated'] = df_merged['co2_rate_interpolated'].fillna(method='ffill')
        df_merged['difference'] = df_merged['co2_rate_init'] - df_merged['co2_rate_interpolated']
        df_last_20 = df_merged.tail(20)
        # print(df_last_20)
        # df_last_20.to_csv('20_derniers_points.csv')

        # Pour chaque donnée (réelle et interpolée), rajouter une ligne au tableau avec la moyenne pour les jours ouvrés, et les weekends
        df_merged.reset_index(inplace=True)
        df_merged['is_weekday'] = df_merged['timestamp'].dt.dayofweek < 5

        df_weekday_or_not = df_merged.groupby(['is_weekday']).mean()
        df_weekday_or_not.reset_index(inplace=True)

        df_merged = df_merged.append(df_weekday_or_not, ignore_index=True)
        # print(df_merged)

        # Bonus: Ajouter un graphe de la différence entre les deux données
        # sns.scatterplot(data=df_merged, x='timestamp', y='difference')
        # plt.show()
