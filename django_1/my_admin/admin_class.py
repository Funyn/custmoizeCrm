# coding:utf-8
from django.db.models.base import ModelBase
from django_day1 import models
from django.shortcuts import HttpResponse, render


enabled_admin = []
show_models = {}


def is_model(model):
    assert isinstance(model, ModelBase), '请检查是否注册的是Django的模型类'


def register( modles_or_iter, admin_class=None):
    if admin_class == None:
        admin_class = BaseAdmin()
    else:
        admin_class = admin_class()
    if not hasattr(modles_or_iter, '__iter__'):
        modles_or_iter = [modles_or_iter]
    for model in modles_or_iter:
        is_model(model)
        admin_class.model = model
        show_models.update({model._meta.model_name:{}})
        show_models[model._meta.model_name].update({'model':admin_class})


class BaseAdmin:
    model = None
    list_display = []
    list_filter = []
    list_per_page = 100
    search_fields = []
    action = []
    action.insert(0,'delete_select_member')
    readonly_field = []
    add_form = True
    readonly_table = False

    def clean(self):
        """
        custmoize validate
        :return: ValidateError if invalid
        """
        pass

    def delete_select_member(self,request,query_set):
        app_name = self.model._meta.app_label
        class_name = self.model._meta.model_name
        return render(request,'action_delete.html',{'models':query_set,
                                                        "app_name":app_name,
                                                        "class_name":class_name})
    delete_select_member.display_name = '删除所选字段'


class CustomerMemberAdmin(BaseAdmin):
    list_display = ['name','id', 'from_address', 'role']
    list_filter = ['from_address','id','name','role']
    list_per_page = 2
    search_fields = ['id']
    readonly_field = ['name']
    readonly_table = True

class CustomeOrderInfoAdmin(BaseAdmin):
    list_display = ['id','content']
    search_fields = ['id']
    list_per_page = 4
    filter_horizontal = ['member']
    # readonly_field = ['member']



register(models.Member, CustomerMemberAdmin)
register(models.AccountRole)
register(models.UserAccount)
register(models.OrderInfo,CustomeOrderInfoAdmin)

