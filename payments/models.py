from django.db import models
from django.conf import settings


from events.models import Event
# Create your models here.

User = settings.AUTH_USER_MODEL


paypal_button_types = (('buy_now', 'buy_now'), ('buy_now_multi', 'buy_now_multi'))


class Payment(models.Model):
    event = models.OneToOneField(Event, models.CASCADE)
    type = models.CharField(max_length=30, choices=paypal_button_types)
    #TODO: Delete or make it so it returns... number or list? Only for dev usage?
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

    def amount_stripe(self):
        print(type(self.amount))
        print(float(self.amount) * 100)
        return float(self.amount) * 100


class TransactionPaypal(models.Model):
    # info about me
    pl_receiver_email = models.CharField(max_length=64)
    pl_receiver_id = models.CharField(max_length=64)
    # info about transaction
    pl_txn_id = models.CharField(max_length=64)
    pl_txn_type = models.CharField(max_length=64)
    # info about buyer
    pl_payer_email = models.CharField(max_length=64)
    pl_payer_id = models.CharField(max_length=64)
    pl_payer_status = models.CharField(max_length=64)
    pl_first_name = models.CharField(max_length=64)
    pl_last_name = models.CharField(max_length=64)
    pl_address_city = models.CharField(max_length=64)
    pl_address_country = models.CharField(max_length=64)
    pl_address_status = models.CharField(max_length=64)
    pl_address_country_code = models.CharField(max_length=64)
    pl_address_name = models.CharField(max_length=64)
    pl_address_street = models.CharField(max_length=64)
    pl_address_zip = models.CharField(max_length=64)
    # info about payment
    pl_custom = models.CharField(max_length=64)
    pl_handling_amount = models.CharField(max_length=64)
    pl_item_name = models.CharField(max_length=64)
    pl_item_number = models.CharField(max_length=64)
    pl_mc_currency = models.CharField(max_length=64)
    pl_mc_fee = models.CharField(max_length=64)
    pl_mc_gross = models.CharField(max_length=64)
    pl_payment_date = models.CharField(max_length=64)
    pl_payment_fee = models.CharField(max_length=64)
    pl_payment_gross = models.CharField(max_length=64)
    pl_payment_status = models.CharField(max_length=64)
    pl_payment_type = models.CharField(max_length=64)
    pl_protection_eligibility = models.CharField(max_length=64)
    pl_quantity = models.CharField(max_length=64)
    pl_shipping = models.CharField(max_length=64)
    pl_tax = models.CharField(max_length=64)
    # Relations to my models
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='transactionpl')
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='transactionpl')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactionpl')
    status = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pricing.payment.event} - {self.buyer}'

    # def is_paid(self, user):
