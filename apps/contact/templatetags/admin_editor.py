from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag()
def admin_editor_url(obj):
    url = reverse('admin:%s_%s_change' % (obj._meta.app_label,
                  obj._meta.model_name), args=[obj.pk])
    return ('<a id="admin_edit" class="btn btn-default'
            'col-md-1" href=%s>Admin edit</a>' % (url))
