from django.shortcuts import render, redirect,  HttpResponse
from django.urls.base import reverse
from django_day1 import handle_logic
from my_admin.utils import obj_slice


# Create your views here.


def app_manage_table(request):
    app_dict = handle_logic.create_manger_table()
    return render(request,'index.html',{'app_dict':app_dict})


def app_manage_model(request, app_name, class_name):
    app_dict = handle_logic.create_manger_table()
    model_admin = app_dict[app_name][class_name]['model']
    keyword = ['page', 'order', 'query','action']
    # page = 0
    # search_value = ''
    # order_key = '-id'
    # filter_keyword = {}
    if request.method == 'GET':
        args = request.GET
        page = args.get('page',0)
        order_key = args.get('order','-id')
        search_value = args.get('query','')
        filter_keyword = handle_logic.legal_filter_list(args,keyword)
        bottom,top = obj_slice(page,model_admin.list_per_page)
        query_set = model_admin.model.objects.filter(**filter_keyword).order_by(order_key)
        if search_value:
            query_set = handle_logic.search_result(query_set,search_value,model_admin)
        model_obj = query_set[bottom:top]
        return render(request,'detail.html', {"model_admin": model_admin,
                                                  "model_obj": model_obj,
                                                  "query_set":query_set,
                                                  "order_key":order_key,
                                                  "app_name":app_name,
                                                  "class_name":class_name,
                                                  })
    if request.method == 'POST':
        action_func_name = request.POST.get('action')
        select_action_list = request.POST.getlist('select_action')
        if not model_admin.readonly_table:
            if action_func_name and select_action_list:
                query_set = model_admin.model.objects.filter(id__in = select_action_list)
                func = getattr(model_admin,action_func_name)
                response = func(request,query_set)
                if isinstance(response,HttpResponse):
                    return response
        return redirect(reverse('model_manage',kwargs={'app_name': app_name, 'class_name': class_name}))


def add_model(request,app_name,class_name):
    app_dict = handle_logic.create_manger_table()
    model_admin = app_dict[app_name][class_name]['model']
    form = handle_logic.dynamic_create_form(model_admin)
    if request.method == 'GET':
        model_admin.add_form = True
        forms = form()
        return render(request, 'add.html', {'forms': forms,
                                            "do":'Add',
                                            "model_admin": model_admin,
                                            "app_name":app_name,
                                            "class_name":class_name
                                            })
    elif request.method == 'POST':
        forms = form(request.POST)
        if forms.is_valid():
            model = model_admin.model()
            for k,v in forms.cleaned_data.items():
                setattr(model,k,v)
            forms.save()
        return redirect(reverse('model_manage', kwargs={'app_name': app_name, 'class_name': class_name}))

def change_model(request,app_name,class_name,nid):
    app_dict = handle_logic.create_manger_table()
    model_admin = app_dict[app_name][class_name]['model']
    model = model_admin.model.objects.filter(id=nid)
    form = handle_logic.dynamic_create_form(model_admin)
    if request.method == 'GET':
        model_admin.add_form = False
        forms = form(instance=model[0])
        return render(request,'change.html',{'forms':forms,
                                             "model_admin": model_admin,
                                             "do": 'Change',
                                             "app_name": app_name,
                                             "class_name": class_name,
                                             "nid":nid,
                                             "errors": forms.errors})
    elif request.method == 'POST':
        forms = form(request.POST,instance=model[0])
        if forms.is_valid():
            forms.save()
            return redirect(reverse('model_manage', kwargs={'app_name': app_name, 'class_name': class_name}))
        else:
            return render(request, 'change.html', {'forms': forms,
                                                   "model_admin": model_admin,
                                                   "do": 'Change',
                                                   "app_name": app_name,
                                                   "class_name": class_name,
                                                   "nid": nid,
                                                   "errors": forms.errors})


def delete_model(request,app_name,class_name,nid):
    app_dict = handle_logic.create_manger_table()
    model_admin = app_dict[app_name][class_name]['model']
    models = model_admin.model.objects.filter(id=nid)
    if request.method == 'GET':
        return render(request,'delete.html',{'models':models,
                                                "verbose_name":model_admin.model._meta.verbose_name,
                                                "app_name":app_name,
                                                "class_name":class_name})
    else:
        models.delete()
        return redirect(reverse('model_manage', kwargs={'app_name': app_name, 'class_name': class_name}))


