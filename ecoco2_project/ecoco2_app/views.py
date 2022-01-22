import imp
from django.shortcuts import render
from django.utils import timezone

import datetime
import pandas as pd
import json

from .models import CO2rate, LowFrequencyCO2rate


def twenty_last_entries(request):
    
    current_tz = timezone.get_current_timezone()
    date_from = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=current_tz)
    date_to = datetime.datetime(2018, 1, 7, 23, 59, 59, tzinfo=current_tz)

    # Récupérer la table de base
    df_init = pd.DataFrame(list(CO2rate.objects.filter(timestamp__gte=date_from, timestamp__lte=date_to).values()))

    # Récupérer la table à basse fréquence
    df_lowf = pd.DataFrame(list(LowFrequencyCO2rate.objects.filter(timestamp__gte=date_from, timestamp__lte=date_to).values()))
    df_lowf = df_lowf.set_index('timestamp')

    # À partir de la table horaire, interpoler les résultats pour (re)obtenir la même fréquence initiale de 30 minutes
    df_reinterpolated = df_lowf.resample('30min').interpolate().bfill()
    print(df_reinterpolated)

    # Différence entre la vraie donnée et la donnée interpolée
    df_merged = pd.merge(df_init, df_reinterpolated, how='left', on='timestamp', suffixes=('_init', '_interpolated'))
    df_merged['co2_rate_interpolated'] = df_merged['co2_rate_interpolated'].fillna(method='ffill')
    df_merged['difference'] = df_merged['co2_rate_init'] - df_merged['co2_rate_interpolated']
    
    df_merged.reset_index(inplace=True)

    # Pour chaque donnée (réelle et interpolée), rajouter une ligne au tableau avec la moyenne pour les jours ouvrés, et les weekends
    df_merged['is_weekday'] = df_merged['timestamp'].dt.dayofweek < 5

    df_weekday_or_not = df_merged.groupby(['is_weekday']).mean()
    df_weekday_or_not = df_weekday_or_not.round(2)
    df_weekday_or_not.reset_index(inplace=True)

    # Afficher le tout
    df_merged['date'] = df_merged['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    df_last_20 = df_merged.tail(20)

    df_weekday_or_not['date'] = df_weekday_or_not['is_weekday'].map(lambda x: 'weekday' if x is True else 'week-end')

    df_last_20 = df_last_20.append(df_weekday_or_not, ignore_index=True)
    print(df_last_20)
    
    last_20_json_records = df_last_20.reset_index().to_json(orient ='records')
    last_20_json = json.loads(last_20_json_records)

    # # Bonus: Ajouter un graphe de la différence entre les deux données
    # sns.scatterplot(data=df_merged, x='timestamp', y='difference')
    # plt.show()

    return render(request, 'list_rates.html', {'data': last_20_json})

