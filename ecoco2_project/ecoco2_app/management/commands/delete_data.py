from django.core.management.base import BaseCommand
from ecoco2_app.models import CO2rate


class Command(BaseCommand):
    def handle(self, **options):

        CO2rate.objects.all().delete()
