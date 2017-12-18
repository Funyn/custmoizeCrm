# coding:utf8
import itertools
from django.utils.deprecation import MiddlewareMixin
class My:
    #
    def __init__(self):
        print('初始化')

    def __call__(self, *args, **kwargs):
        print('调用类')

class M(My):

    def __init__(self):
        # super(M,self).__init__()
        print(super(M,self).__init__())
        print('chushihua')
# m = M()
# m1 = M()
# print(list(itertools.chain([22], (1,2,3,4))))
from django.test import TestCase
# Create your tests here.
import json
from datetime import date
from datetime import datetime
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):

        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)

# print(__import__('apps'))

class FirstMiddleware(MiddlewareMixin):

    def process_request(self,request):
        print(request)

    def process_view(self,request,callback,callback_args,callback_kwargs):
        print('处理类')

    def process_response(self,request,response):
        print(request)
        print(response)
        return response

from django.core.signals import request_started
from django.db.models.signals import post_delete, pre_init
from django.core.handlers.wsgi import WSGIHandler
def start_request(sender, **kwargs):
    print('what is this',sender,kwargs)
# import uuid
# print(isinstance(uuid.uuid4(),type(uuid.uuid4())))
# print()
def wrap(sender,**kwargs):
    print('初始化数据模型')
    return wrap


# pre_init.connect(wrap)
# request_started.connect(start_request)
# import inspect
# # print(inspect.getargspec(start_request))
# print(hasattr(start_request, '__func__'))

# import requests
#
# response = requests.get('https://www.amazon.cn/')
# print(response.text)
b = type('MyClass',(object,), dict(hello='www'))
print(b.__dict__)

a = [[],[],[],]
import random
class A:
    model = 'ccc'
    weigth = 6
    pass
b = A()
setattr(b,'weigth',5)
print(A().weigth)

from urllib.parse import quote

obj = (1,'g')
c = (2,'b')
w = zip(obj,c)
print(list(w)[0])


