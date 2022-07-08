from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.CharField(
        'адрес',
        max_length=100,
        unique=True,
    )
    lat = models.DecimalField(
        'широта', decimal_places=2, max_digits=9, null=True, blank=True
    )
    lon = models.DecimalField(
        'долгота', decimal_places=2, max_digits=9, null=True, blank=True
    )

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'
