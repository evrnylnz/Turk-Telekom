# app/management/commands/add_routers.py
from django.core.management.base import BaseCommand

from app.models import RouterBrand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        routers = {
            'Cisco': ['2960x', '3750', '4510 Gi4', '4510 Gi5', '4510 Gi6'],
            'Huawei': ['AR2220']
        }

        for brand_name, router_names in routers.items():
            brand = RouterBrand.objects.get(name=brand_name)
            for router_name in router_names:
                router, created = brand.router_set.get_or_create(model_name=router_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added router {router.model_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Router {router.model_name} already exists'))
