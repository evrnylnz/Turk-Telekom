import pandas as pd

from app.models import Province, District

provinces = pd.read_csv("../uavt_il.csv", sep=";")
districts = pd.read_csv("../uavt_ilce.csv", sep=';')

db = {}
for index, province in provinces.iterrows():
    district_array = []
    province_name = province['adi']
    for _, district in districts.iterrows():
        if district['il_kod'] == province['kodu']:
            district_array.append(district['ad'])

    db[province_name] = district_array

for province_name, districts in db.items():
    province, _ = Province.objects.get_or_create(name=province_name)
    for district_name in districts:
        district, _ = District.objects.get_or_create(name=district_name, province=province)

print('Finished')
