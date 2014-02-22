import binascii
import os

from hashlib import sha1

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AnonymousUser


# Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True, null=False, blank=False)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='auth_token', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    # TODO: It is possiple use https://github.com/selwin/django-user_agents/tree/master/django_user_agents or
    # https://github.com/selwin/python-user-agents for parse
    # Limited size to 256
    user_agent = models.CharField(max_length=256, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        """
        Random id generating
        """
        return binascii.hexlify(os.urandom(20))

    def __unicode__(self):
        return self.key


class AnonymousToken(object):
    key = None
    user = AnonymousUser
    creted_at = None
    is_active = False
    user_agent = None

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
