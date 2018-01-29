from django.contrib import admin

# Register your models here.


from .models import Payment, Pricing

admin.site.register(Payment)
admin.site.register(Pricing)
