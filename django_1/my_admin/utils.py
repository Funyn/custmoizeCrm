# coding:utf-8
from urllib.parse import quote


def path_link(args, obj=None):
    path = ''
    if args:
        for key, value in args.items():
            if key != obj:
                path += '&%s=%s' % (key, quote(value))
    return path


def obj_slice(page,pre_page):
    page = int(page)
    bottom = page*pre_page
    top = (page+1)*pre_page
    return bottom, top


def order_name(order_key,field_name):
    if order_key != field_name:
        return field_name
    else:
        return '-'+field_name

