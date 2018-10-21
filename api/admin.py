# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import *

# Register your models here.

class UserBaseAdmin(UserAdmin):
    list_display = ('id','username','first_name','last_name','birthday')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        (_('Personal info'),
            {'fields': ('first_name', 'last_name', 'birthday','avatar',
            'avatar_url','opt')}),
        (_('Permissions'), 
            {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), 
            {'fields': ('last_login', 'date_joined')}),
        )
    # inlines = (OrderInline,)

class TestHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','name_of_test','creation_date','status')
class VisitHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','location','creation_date','visit_reason')
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id','name','address','phone')
    
        
admin.site.register(UserBase, UserBaseAdmin)
admin.site.register(TestHistory, TestHistoryAdmin)
admin.site.register(VisitHistory, VisitHistoryAdmin)
admin.site.register(Location, LocationAdmin)
