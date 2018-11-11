# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import pprint
from rest_framework.authtoken.models import Token

class UserBase(AbstractUser):
    CONST_ROLE_PATIENT = 10
    CONST_ROLE_DOCTOR =0

    CONST_ROLE = (
        (CONST_ROLE_PATIENT,_('Patient')),
        (CONST_ROLE_DOCTOR,_('Doctor'))
    ) 
    role = models.PositiveSmallIntegerField(choices=CONST_ROLE, default=CONST_ROLE_PATIENT)
    email = models.EmailField(_('email address'), null=True, blank=True)
    birthday = models.DateField(null=True, blank=False)
    avatar = models.ImageField(help_text=_('Picture shall be squared, max 640*640, 500k'), upload_to='avatars',
                                 null=True, blank=True)
    avatar_url = models.CharField(max_length=200, null=True, blank=True, default=settings.MEDIA_URL+'avatar_defautl.png')
    opt = models.CharField(max_length=255, null=True, blank=True)
    block_chain_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=255, unique=True, null=True, blank=True)

    emergency_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    emergency_address = models.CharField(max_length=255, unique=True, null=True, blank=True)
    emergency_phone = models.CharField(max_length=255, unique=True, null=True, blank=True)
    emergency_relationship = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name,self.last_name)

    @property
    def token(self):
        return self.auth_token.key

@receiver(post_save, sender=UserBase)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class TestHistory(models.Model):
    CONST_NAME_HIV           = 0
    CONST_NAME_HEPATITIS     = 10   #Viem gan
    CONST_NAME_POLIOMYELITIS = 20 #Viem tuy
    CONST_NAME_BRAIN_FEVER = 30 #Viem nao

    CONST_NAME = (
        (CONST_NAME_HIV, _('HIV')),
        (CONST_NAME_HEPATITIS, _('Hepatitis')),
        (CONST_NAME_POLIOMYELITIS, _('Poliomyelitis')),
        (CONST_NAME_BRAIN_FEVER, _('Brain fever')),
    )

    CONST_STATUS_TESTING = 10 # Test
    CONST_STATUS_PENDING =20 # Co ket qua cho tra tien
    CONST_STATUS_RATING =30 # Cho rating
    CONST_STATUS_CLOSE =40 
    CONST_STATUS_GOOD =10
    CONST_STATUS_BAD = 0

    CONST_STATUS = (
        (CONST_STATUS_TESTING,_('Testing')),
        (CONST_STATUS_PENDING,_('Pending')),
        (CONST_STATUS_RATING,_('Rating')),
        (CONST_STATUS_CLOSE,_('Close')),
    )
    CONST_RESULT =(
        (CONST_STATUS_GOOD,_('Good')),
        (CONST_STATUS_BAD,_('Bad'))
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    name_of_test = models.PositiveSmallIntegerField(choices=CONST_NAME)
    status =  models.PositiveSmallIntegerField(choices=CONST_STATUS, default=CONST_STATUS_TESTING)
    result =  models.PositiveSmallIntegerField(choices=CONST_RESULT,null=True, blank=True)
    user = models.ForeignKey("UserBase",related_name="patient_test_history")
    doctor = models.ForeignKey("UserBase",related_name="doctor_test_history",null=True, blank=True)
    price = models.IntegerField(default=0)
    doctor_star = models.PositiveSmallIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    abi = models.CharField(max_length=2000, null=True, blank=True)

@receiver(pre_save, sender=TestHistory)
def update_status(sender, instance=None, created=False, **kwargs):
    if not instance.doctor_star==None:
        instance.status=TestHistory.CONST_STATUS_CLOSE

class VisitHistory(models.Model):
    user          = models.ForeignKey("UserBase",related_name="visit_history")
    creation_date = models.DateField(auto_now_add=True)
    visit_reason  = models.CharField(max_length=255, unique=True, null=True, blank=True)
    note          = models.CharField(max_length=255, unique=True, null=True, blank=True)
    location      = models.ForeignKey("Location")

class Location(models.Model):
    name    = models.CharField(max_length=255, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, unique=True, null=True, blank=True)
    phone   = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

