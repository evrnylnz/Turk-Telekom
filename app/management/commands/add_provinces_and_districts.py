# app/management/commands/add_provinces_and_districts.py
import pandas as pd
from django.core.management.base import BaseCommand

from app.models import Province, District


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        provinces = pd.read_csv("uavt_il.csv", sep=";")
        districts = pd.read_csv("uavt_ilce.csv", sep=';')

        db = {}
        for index, province in provinces.iterrows():
            district_array = []
            province_name = province['adi']
            for idx, district in districts.iterrows():
                if district['il_kod'] == province['kodu']:
                    district_array.append(district['ad'])
            db[province_name] = district_array

        for province_name, district_names in db.items():
            province, created = Province.objects.get_or_create(name=province_name)
            self.stdout.write(self.style.SUCCESS(f'Added province {province_name}'))
            for district_name in district_names:
                district, created = District.objects.get_or_create(name=district_name, province=province)
                self.stdout.write(self.style.SUCCESS(f'  Added district {district_name} to {province_name}'))

        self.stdout.write(self.style.SUCCESS('Finished importing provinces and districts'))
