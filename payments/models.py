from django.db import models

from events.models import Event
# Create your models here.


paypal_button_types = (('buy_now', 'buy_now'), ('buy_now_multi', 'buy_now_multi'))


class Payment(models.Model):
    event = models.OneToOneField(Event, models.CASCADE)
    type = models.CharField(max_length=30, choices=paypal_button_types)
    price = models.TextField(help_text='Seperate each item by comma')

    def __str__(self):
        return f'{self.event} - {self.type}: {self.price}'

    def get_price(self):
        if self.type == 'buy_now':
            return self.price
        if self.type == 'buy_now_multi':
            return self.price.split(",")


class Pricing(models.Model):
    title = models.CharField(max_length=64)
    amount = models.CharField(max_length=64)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='pricing')

    def __str__(self):
        return f'{self.payment.event} - {self.title}: {self.amount}'
