from django.db import models

class StockDB(models.Model):
    name = models.CharField('name', max_length=200)
    code = models.CharField('code', max_length=20)
    type = models.CharField('type', max_length=100)
    price = models.FloatField('latest_price', default=0)
    change = models.FloatField('change_mount', default=0)
    priceofYest = models.FloatField('yesterday_close_price', default=0)
    priceofToda = models.FloatField('today_open_price', default=0)
    priceofHigh = models.FloatField('highest_price', default=0)
    priceofLow = models.FloatField('lowest_price', default=0)
    inflow = models.FloatField('net_inflow', default=0)
    turnoverAmount = models.FloatField('turnover_amount', default=0)
    turnoverVolume = models.FloatField('turnover_volume', default=0)
    turnoverRate = models.FloatField('turnover_rate', default=0)

    def __unicode__(self):
        return self.name

from django.contrib import admin
admin.site.register(StockDB)