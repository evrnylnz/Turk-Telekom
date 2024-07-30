from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RouterBrand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Router(models.Model):
    brand = models.ForeignKey(RouterBrand, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=50)

    def __str__(self):
        if self.brand.name == self.model_name or self.model_name == '':
            return self.brand.name
        return f"{self.brand.name} {self.model_name}"


class Device(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)

    station = models.CharField(max_length=50, blank=True, null=True)
    location_name = models.CharField(max_length=50, blank=True, null=True)
    location_floor = models.CharField(max_length=50, blank=True, null=True)

    router_brand = models.ForeignKey(RouterBrand, on_delete=models.CASCADE, blank=True, null=True)
    router_model = models.ForeignKey(Router, on_delete=models.CASCADE, related_name="primary_devices", blank=True, null=True)
    router_count = models.CharField(max_length=50, blank=True, null=True)
    number_of_ports = models.CharField(max_length=50, blank=True, null=True)

    connected_routers = models.ManyToManyField(Router, related_name="connected_devices", blank=True)
    connection_port = models.CharField(max_length=50, blank=True, null=True)
    connected_router_location = models.CharField(max_length=50, blank=True, null=True)

    loopback_ip = models.CharField(max_length=50, blank=True, null=True)
    vlan = models.CharField(max_length=50, blank=True, null=True)
    connection = models.CharField(max_length=50, blank=True, null=True)
    energy_type = models.CharField(max_length=50, blank=True, null=True)
    temos = models.CharField(max_length=50, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.loopback_ip}"
    
class Trash(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.device.loopback_ip if self.device and self.device.loopback_ip else 'Unknown Device'