from django import forms
from .models import Province, District, RouterBrand, Router, Device

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = [field.name for field in Province._meta.get_fields() if field.concrete]

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = [field.name for field in District._meta.get_fields() if field.concrete]

    def __init__(self, *args, **kwargs):
        province_id = kwargs.pop('province_id', None)
        super(DistrictForm, self).__init__(*args, **kwargs)
        if province_id:
            self.fields['district'].queryset = District.objects.filter(province_id=province_id)

class RouterBrandForm(forms.ModelForm):
    class Meta:
        model = RouterBrand
        fields = [field.name for field in RouterBrand._meta.get_fields() if field.concrete]

class RouterForm(forms.ModelForm):
    class Meta:
        model = Router
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        brand_id = kwargs.pop('brand_id', None)
        super(RouterForm, self).__init__(*args, **kwargs)
        if brand_id:
            self.fields['router'].queryset = Router.objects.filter(brand_id=brand_id)

class DeviceForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=True)
    district = forms.ModelChoiceField(queryset=District.objects.none(), required=True)
    router_brand = forms.ModelChoiceField(queryset=RouterBrand.objects.all(), required=True)
    router_model = forms.ModelChoiceField(queryset=Router.objects.none(), required=True)

    class Meta:
        model = Device
        fields = [field.name for field in Device._meta.get_fields() if field.concrete]
        exclude = ['deleted'] 
        widgets = {
            'connected_routers': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)

        # Filtering districts based on the selected province
        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['district'].queryset = District.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.province.district_set.order_by('name')

        # Filtering router models based on the selected router brand
        if 'router_brand' in self.data:
            try:
                brand_id = int(self.data.get('router_brand'))
                self.fields['router_model'].queryset = Router.objects.filter(brand_id=brand_id).order_by('model_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['router_model'].queryset = self.instance.router_brand.router_set.order_by('model_name')