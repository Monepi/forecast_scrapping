# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Weather(models.Model):
    date = models.DateField()
    min_tem = models.FloatField()
    max_temp = models.FloatField()
    wind = models.FloatField()
    rain = models.FloatField()

