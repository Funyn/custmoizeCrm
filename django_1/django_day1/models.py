from django.db import models
from django.utils.timezone import now


class UserAccount(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=30, null=False, default='88888888')
    create_time = models.DateField(default=now())
    last_login_time = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(to='AccountRole',to_field='id')

    def __str__(self):
        return '{username}'.format(username=self.username)


class AccountRole(models.Model):
    role_name = models.CharField(max_length=64)

    def __str__(self):
        return '{role_name}'.format(role_name=self.role_name)


class WorkRole(models.Model):
    work_role = models.CharField(max_length=64)

    def __str__(self):
        return '{work_role}'.format(work_role=self.work_role)


class UserDetail(models.Model):
    phone = models.CharField(max_length=18, null=True)
    member = models.OneToOneField('Member',to_field='id')


class OrderInfo(models.Model):
    content = models.TextField(null=False, default='工作内容如下')
    order_address = models.CharField(max_length=64, null=False, default='岭澳一号机')
    create_time = models.DateTimeField(default=now())
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=now())
    status = models.IntegerField(choices=((0, '编辑订单'),(1, '审核订单'),(2, '订单已审核'),(3, '允许工作'),(4, '工作中'),(5, '工作结束'),(6, '关闭订单')))
    member = models.ManyToManyField('Member')
    responsible_person = models.ForeignKey(to='UserAccount', to_field='id')


class Company(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)
    address = models.CharField(max_length=64, null=False, unique=True)

    def __str__(self):
        return '{address}'.format(address=self.address)


class Member(models.Model):
    name = models.CharField(max_length=64, null=False)
    role = models.ForeignKey(to='WorkRole',to_field='id')
    from_address = models.ForeignKey(to='Company', to_field='id')
    account = models.OneToOneField('UserAccount', null=True)

    def __str__(self):
        return '{name}'.format(name=self.name)





