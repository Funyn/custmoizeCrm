from django.conf.urls import url

from my_admin import views

urlpatterns = [
    url(r'admin/$', views.app_manage_table, name='table_manage'),
    url(r'admin/(?P<app_name>\w+)/(?P<class_name>\w+)/$', views.app_manage_model, name='model_manage'),
    url(r'admin/(?P<app_name>\w+)/(?P<class_name>\w+)/add/', views.add_model, name='model_add'),
    url(r'admin/(?P<app_name>\w+)/(?P<class_name>\w+)/(?P<nid>\d+)/change/', views.change_model, name='model_change'),
    url(r'admin/(?P<app_name>\w+)/(?P<class_name>\w+)/(?P<nid>\d+)/delete/', views.delete_model, name='model_delete'),
]


