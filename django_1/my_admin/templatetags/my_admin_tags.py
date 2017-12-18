#coding:utf-8
from django import template
from django.utils.safestring import mark_safe
from urllib.parse import quote
from my_admin.utils import  path_link,order_name
from django.db.models.fields.related import ForeignKey


register = template.Library()


@register.simple_tag
def bulid_obj_meta(model_admin):
    ret = model_admin.model._meta.verbose_name
    ret = ret.capitalize()
    return ret


@register.simple_tag
def bulid_href_to_model(request, model_admin):
    url = request.path+model_admin["model"].model._meta.app_label+'/'+model_admin['model'].model._meta.model_name
    return url


@register.simple_tag
def bulid_table_field(request, model_admin, model_obj,order_key,flags=None):
    display_list = model_admin.list_display
    path = path_link(request.GET,'order')
    result = ''
    if display_list:
        if not flags:
            field_list = [field for field in model_admin.model._meta.fields]
            field_name_list = list(map(lambda field:field.name,field_list))
            for field in display_list:
                if field in field_name_list:
                    index_key = field_name_list.index(field)
                    field_obj = field_list[index_key]
                    field_name = order_name(order_key,field)
                    result += '<th><a href="?order={field_name}{path}" >{verbose_name}</a></th>'.format(
                        field_name=field_name,path=path,verbose_name=field_obj.verbose_name)
        else:
            for model in model_obj:
                result += '<tr>'
                result += '<td><input type="checkbox" name="select_action" value="%s" /></td>'%model.id
                for index,field in enumerate(display_list):
                    value = getattr(model,field)
                    if index != 0:
                        result += '<td>'+str(value)+'</td>'
                    else:
                        result += '<td><a href="%s%s/change/">'%(request.path,model.id) + str(value) + '</a></td>'
                result += '</tr>'
    else:
        if not flags:
            result = '<th>'+model_admin.model._meta.verbose_name+'</th>'
        else:
            for model in model_obj:
                result += '<tr>'
                result += '<td><input type="checkbox" name="select_action" value="%s" /></td>' % model.id
                result += '<td><a href="%s%s/change/">'%(request.path,model.id)+str(model)+'</a></td>'
                result += '</tr>'
    return mark_safe(result)


@register.simple_tag
def bulid_tag_for_list_filter(model_admin,obj,request):
    args = request.GET
    path = path_link(args,obj)
    result = ''
    model = model_admin.model
    for field in model._meta.fields:
        if obj == field.name:
            if isinstance(field,ForeignKey):
                query_set = field.related_model.objects.all()
                for query in query_set:
                    result += '<a href="?{field_name}={query_id}{path}" class="list-group-item" >{query}</a>'.format(
                        field_name=field.name,query_id=query.id ,query=query,path=path)
            else:
                query_set = field.model.objects.all()
                for query in query_set:
                    attr = getattr(query,field.name)
                    result += '<a href="?{field_name}={url_attr}{path}" class="list-group-item" >{attr}</a>'.format(
                        field_name=field.name,url_attr=quote(str(attr)),attr=attr,path=path)
    return mark_safe(result)


@register.simple_tag
def build_page_num_link(request):
    path = path_link(request.GET,'page')
    return path


@register.simple_tag
def ret_range_num(request,model_admin,query_set):
    from django.core.paginator import Paginator
    current_page = int(request.GET.get('page','0'))
    page_obj = Paginator(query_set,model_admin.list_per_page)
    if page_obj.num_pages > 0 and page_obj.num_pages < 5:
        current_page_range = list(range(0,page_obj.num_pages))
    elif current_page - 2 < 0 :
        current_page_range = list(range(0,page_obj.num_pages))[0:5]
    elif current_page + 3 > page_obj.num_pages:
        current_page_range = list(range(0,page_obj.num_pages))[current_page-3:page_obj.num_pages]
        if len(current_page_range) < 5:
            current_page_range = list(range(0, page_obj.num_pages))[current_page - 4:page_obj.num_pages]
    else:
        current_page_range = list(range(0,page_obj.num_pages))[current_page-2:current_page+3]
    return current_page_range


@register.simple_tag
def current_page(request):
    current_pg = int(request.GET.get('page', '0'))
    return current_pg

@register.simple_tag
def prepage(request):
    current_page = int(request.GET.get('page','0'))
    if current_page != 0:
        pre_page = current_page - 1
    else:
        pre_page = 0
    return pre_page


@register.simple_tag
def nextpage(request,model_admin,query_set):
    from django.core.paginator import Paginator
    current_page = int(request.GET.get('page','0'))
    page_obj = Paginator(query_set,model_admin.list_per_page)
    max_page = page_obj.num_pages-1
    if current_page != max_page:
        next_page = current_page + 1
    else:
        next_page = max_page
    return next_page

@register.simple_tag
def bulid_action_to_view(request):
    result = ''
    for key,value in request.GET.items():
        if key == 'query':
            continue
        result += '<input type="hidden" name="{key}" value="{value}"/>'.format(key=key,value=value)
    return mark_safe(result)


@register.simple_tag
def action_display_name(model_admin,action):
    action_func = getattr(model_admin,action)
    display_name = getattr(action_func,'display_name',action)
    return display_name


@register.simple_tag
def bulid_m2m(model_admin,form_field,nid=None,chosen=None):
    form_field_name = form_field.name
    m2m_fks = model_admin.model._meta.local_many_to_many
    exist_obj_id = []
    if nid:
        exist_obj = model_admin.model.objects.filter(id=nid).first()
        exist_obj_id = [obj.id for obj in getattr(exist_obj,form_field_name).all()]
    for fk in m2m_fks:
        if fk.related_model._meta.model_name == form_field_name:
            if nid and chosen :
                query_set = fk.related_model.objects.filter(id__in=exist_obj_id)
            elif nid:
                query_set = fk.related_model.objects.exclude(id__in=exist_obj_id)
            else:
                query_set = fk.related_model.objects.all() or []
            return query_set


def recursive_related_objs_lookup(objs):
    ul_ele = ''
    for obj in objs:
        sub_ul_ele = '<ul><li>%s  : %s'%(obj._meta.verbose_name,'<a href="#">%s</a>'%obj)
        m2m_fields = obj._meta.local_many_to_many
        for field in m2m_fields:
            query_set = getattr(obj,field.name).select_related()
            m2m_sub_ul_ele = '<ul>'
            for query in query_set:
                sub_li_ele = '<li>%s : %s</li>'%(obj._meta.verbose_name,query.__str__())
                m2m_sub_ul_ele += sub_li_ele
            m2m_sub_ul_ele += '</ul>'
            sub_ul_ele += m2m_sub_ul_ele
        for related_obj in obj._meta.related_objects:
            if "ManyToManyRel" in related_obj.__str__():
                if hasattr(obj,related_obj.get_accessor_name()):
                    accessor_obj = getattr(obj,related_obj.get_accessor_name())
                    if hasattr(accessor_obj,'select_related'):
                        query_set = accessor_obj.select_related()
                        m2m_sub_ul_ele = '<ul>'
                        for query in query_set:
                            m2m_sub_li_ele = '<li>%s : %s</li>' % (obj._meta.verbose_name, query.__str__())
                            m2m_sub_ul_ele += m2m_sub_li_ele
                        m2m_sub_ul_ele += '</ul>'
                        sub_ul_ele += m2m_sub_ul_ele
            elif hasattr(obj,related_obj.get_accessor_name()):
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                if hasattr(accessor_obj, 'select_related'):
                    query_set = accessor_obj.select_related()
                else:
                    query_set = [accessor_obj]
                if len(query_set) >0:
                    node = recursive_related_objs_lookup(query_set)
                    sub_ul_ele += node
        sub_ul_ele += '</li></ul>'
        ul_ele += sub_ul_ele
    return ul_ele

@register.simple_tag
def display_obj_related(objs):
    '''把对象及所有相关联的数据取出来'''
    if objs:
        result =  recursive_related_objs_lookup(objs)
        ret = result.replace('<ul></ul>','')
        return mark_safe(ret)

