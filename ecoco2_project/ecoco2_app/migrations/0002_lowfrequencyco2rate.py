# Generated by Django 3.2.11 on 2022-01-22 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoco2_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LowFrequencyCO2rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('co2_rate', models.FloatField(default=0.0)),
            ],
        ),
    ]
