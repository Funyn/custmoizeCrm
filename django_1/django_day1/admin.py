from django.contrib import admin

# Register your models here.
from django_day1 import models


class CustomeMemberAdmin(admin.ModelAdmin):
    list_display = ['name','from_address','role']
    list_filter = ('from_address','id')
    search_fields = ['id']
    list_per_page = 4


class CustomeOrderInfoAdmin(admin.ModelAdmin):
    list_display = ['id','content']
    search_fields = ['id']
    list_per_page = 4
    filter_horizontal = ['member']


admin.site.register(models.Member,CustomeMemberAdmin)
admin.site.register(models.WorkRole)
admin.site.register(models.UserAccount)
admin.site.register(models.OrderInfo,CustomeOrderInfoAdmin)