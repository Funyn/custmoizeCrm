# coding:utf-8
from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator,BaseValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible

@deconstructible
class MyValidator:
    message = _('Enter only digits separated by commas.')
    code = 'invalid'

    def __init__(self):
        print('初始化')

    def __call__(self,value):
        self.compare()
        raise ValidationError('你错的真离谱', code=self.code)

    def compare(self):
        print('实现这个方法就没错')
        return 'True or False'

class LoginForm(forms.Form):

    user = forms.CharField(validators=(MyValidator(),))
    # url = forms.DateTimeField(widget=widgets.CheckboxSelectMultiple(choices=((1,'ww'),(2,'cc'))))
    phone = forms.RegexField(regex=r'^\d{4}$',error_messages=({'invalid':'这不符合规则'}))


