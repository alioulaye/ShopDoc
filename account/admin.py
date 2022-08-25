from atexit import register
from django.contrib import admin

from account.models import Shopper

# Register your models here.
admin.site.register(Shopper)