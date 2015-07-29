from django.contrib import admin

from apps.contact.models import MyMiddle, Contact, Signal
# Register your models here.


admin.site.register(Contact)
admin.site.register(MyMiddle)
admin.site.register(Signal)
