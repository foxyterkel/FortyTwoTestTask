from django.contrib import admin

from apps.contact.models import RequestEntry, Contact, Signal
# Register your models here.


class RequestEntryAdmin(admin.ModelAdmin):
    list_display = ('url_path', 'created_at')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'contacts',
                    'bio', 'email', 'jaber', 'skype', 'other_contacts')

admin.site.register(Contact, ContactAdmin)
admin.site.register(RequestEntry, RequestEntryAdmin)
admin.site.register(Signal)
