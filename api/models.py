# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class UserBase(AbstractUser):
    email = models.EmailField(_('email address'), null=True, blank=True)
    birthday = models.DateField(null=True, blank=False)
    avatar = models.ImageField(help_text=_('Picture shall be squared, max 640*640, 500k'), upload_to='avatars',
                                 null=True, blank=True)
    avatar_url = models.CharField(max_length=200, null=True, blank=True, default=settings.MEDIA_URL+'avatar_defautl.png')
    opt = models.CharField(max_length=255, null=True, blank=True)
    block_chain_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name,self.last_name)