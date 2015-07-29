from django.utils.timezone import now


def my_receiver(sender, **kargs):
    from apps.contact.models import Signal
    try:
        if kargs['created']:
            action = 'create'
        else:
            action = 'save'
    except:
        action = 'delete'
    Signal.objects.create(model=sender._meta.model_name,
                          action=action, time=now())
