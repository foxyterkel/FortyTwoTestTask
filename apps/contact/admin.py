from django.contrib import admin

from apps.contact.models import RequestEntry, Contact, Signal
# Register your models here.


class RequestEntryAdmin(admin.ModelAdmin):
    list_display = ('url_path', 'created_at')

admin.site.register(Contact)
admin.site.register(RequestEntry, RequestEntryAdmin)
admin.site.register(Signal)
