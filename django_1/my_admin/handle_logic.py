from my_admin.admin_class import show_models
from django.db.models.query import Q
from django.utils.translation import gettext as _


def create_manger_table():
    app_dict = {}
    for model_name,model_value in show_models.items():
        model_app = model_value['model'].model._meta.app_label
        app_dict.update({model_app:show_models})
    return app_dict


def search_result(query_set,search_value,model_admin):
    search_fields = model_admin.search_fields
    q = Q()
    q.connector = 'OR'
    for field in search_fields:
        q.children.append((field+'__icontains',search_value,))
    result = query_set.filter(q)
    return result


def legal_filter_list(args,keyword):
    filter_keyword = {}
    for key, value in args.items():
        if key in keyword:
            continue
        filter_keyword.update({key: value})
    return filter_keyword


def dynamic_create_form(model_admin):
    from django import forms
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs.update({'class':'form-control'})
            if  model_admin.readonly_table:
                field_obj.widget.attrs['disabled'] = 'disabled'
            elif not model_admin.add_form and field_name in model_admin.readonly_field:
                field_obj.widget.attrs['disabled'] = 'disabled'
        return forms.ModelForm.__new__(cls)


    def default_clean(self):
        error_list = []
        if model_admin.readonly_table:
            if self.data:
                error_list.append(forms.ValidationError(_('The %(table_name)s field is readonly, cannot be modified'),
                                                code='readonly_table',params={"table_name":model_admin.model._meta.verbose_name}))
        else:
            for field_name,initial_val in self.initial.items():
                if field_name in model_admin.readonly_field:
                    if self.data[field_name] != initial_val:
                        error_list.append(
                            forms.ValidationError(_('The %(field_name)s field is readonly, cannot be modified'),
                                                    code='readonly_field',params={"field_name":field_name}))
        try:
            model_admin.clean()
        except forms.ValidationError as e:
            error_list.append(e)
        if error_list:
            raise forms.ValidationError(error_list)
    class Meta:
        model = model_admin.model
        fields = '__all__'
    attrs = {'Meta':Meta}
    form_class = type('DynamicForm',(forms.ModelForm,),attrs)
    setattr(form_class,'__new__',__new__)
    setattr(form_class,'clean',default_clean)
    return form_class