from django.contrib import admin

from apps.contact.models import RequestEntry, Contact, Signal
# Register your models here.


admin.site.register(Contact)
admin.site.register(RequestEntry)
admin.site.register(Signal)
