import json
import os
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from countries.models import Country, Region


class Command(BaseCommand):
    help = "Loads country data from a JSON file."

    IMPORT_FILE = os.path.join(settings.BASE_DIR, "..", "data", "countries.json")

    def get_data(self):
        r = requests.get(
            url = 'https://storage.googleapis.com/dcr-django-test/countries.json',
            headers = {'Accept' : 'application/json'}
        )
        if r.status_code == 200:
            return r.json()
        else:
            return {} # API returned no data

    def handle(self, *args, **options):
        data = self.get_data()
        for row in data:
            region, region_created = Region.objects.get_or_create(name=row["region"])
            if region_created:
                self.stdout.write(
                    self.style.SUCCESS("Region: {} - Created".format(region))
                )
            country, country_created = Country.objects.get_or_create(
                name=row["name"],
                defaults={
                    "alpha2Code": row["alpha2Code"],
                    "alpha3Code": row["alpha3Code"],
                    "population": row["population"],
                    "region": region,
                    "topLevelDomain": (row["topLevelDomain"]+[''])[0], # Get first top level domain from list or default to empty string
                    "capital" : row["capital"]
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "{} - {}".format(
                        country, "Created" if country_created else "Updated"
                    )
                )
            )
