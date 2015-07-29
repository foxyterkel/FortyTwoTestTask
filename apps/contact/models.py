from django.db import models
from django.utils import timezone
from django.core.validators import validate_email, MinLengthValidator, \
    RegexValidator


def generate_path(self, filename):
    url = 'pictures/%s/%s' % (self.email, filename)
    return url


class Contact(models.Model):
    first_name = models.CharField(max_length=50,
                                  validators=[MinLengthValidator(2), ])
    last_name = models.CharField(max_length=50,
                                 validators=[MinLengthValidator(2), ])
    birth_date = models.DateField(default=timezone.now)
    contacts = models.CharField(max_length=13,
                                validators=[RegexValidator('[+]\d{12}'), ])
    bio = models.TextField(max_length=250,
                           validators=[MinLengthValidator(10), ])
    email = models.EmailField(validators=[validate_email, ], unique=True)
    jaber = models.CharField(max_length=100, default='example@mail.ru',
                             blank=True)
    skype = models.CharField(max_length=100, default='example',
                             blank=True)
    other_contacts = models.TextField(max_length=250, blank=True)
    photo = models.ImageField(upload_to=generate_path, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class MyMiddle(models.Model):
    body = models.CharField(max_length=250)
    watched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False,
                                      blank=True, null=True)

    class Meta:
        ordering = ['-created_at', ]
