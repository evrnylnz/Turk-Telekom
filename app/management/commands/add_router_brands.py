# app/management/commands/add_router_brands.py
from django.core.management.base import BaseCommand

from app.models import RouterBrand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        brands = ["Cisco", "Huawei", "LANTECH"]

        for brand in brands:
            brand, created = RouterBrand.objects.get_or_create(name=brand)
            router, created = brand.router_set.get_or_create(model_name=brand)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added router brand {brand.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Router brand {brand.name} already exists'))
