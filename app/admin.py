from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SessionLevel)
admin.site.register(BankUser)
admin.site.register(BankAccount)
admin.site.register(BankTransaction)
