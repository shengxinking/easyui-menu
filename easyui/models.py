#coding:utf-8
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse_lazy

from .mixins.model_mixins import ModelMixin
# Create your models here.
class Menu(ModelMixin, models.Model):
    """
    menu model
    reverse: args and kwargs cannot be passed to reverse() at the same time.
    这里只是用了kwargs
    """
    text = models.CharField('菜单名', max_length=100, help_text='最多100个英文字母长')
    is_root = models.BooleanField('是否为根节点', help_text='这个不添的，form中缺省处理', default=False)
    parent_id = models.IntegerField('父ID')
    namespace = models.CharField('APP名', max_length=100, blank=True)
    viewname = models.CharField('view名', max_length=100, blank=True)
    kwargs = models.CharField('附加参数', max_length=100, blank=True)
    is_system = models.BooleanField('是否为系统菜单', default=False, blank=True, help_text='系统菜单只对超级用户和后台用户显示', editable=False)

    def get_absolute_url(self):
        return reverse_lazy('easyui:MenuListView')

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    def test(self, name):
        return name
        #raise Exception(a)



class UserMenu(ModelMixin, models.Model):
    """
    用户的菜单权限
    """
    user = models.ForeignKey(User, verbose_name='用户', unique=True)
    menus_show = models.TextField('菜单显示权限', help_text='JSON格式的字符串，在菜单显示', blank=True)
    menus_checked = models.TextField('菜单checked', help_text='JSON格式的字符串, checked用户权限配置', blank=True)
    def get_absolute_url(self):
        return reverse_lazy('easyui:UserMenuListView')

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = '用户菜单权限'
        verbose_name_plural = verbose_name
        #permissions = (
        #('list_myusermenu', '查看'+verbose_name),
        #)

class GroupMenu(ModelMixin, models.Model):
    """
    用户的菜单权限
    """
    group = models.ForeignKey(Group, verbose_name='用户组', unique=True)
    menus_show = models.TextField('菜单显示权限', help_text='JSON格式的字符串，在菜单显示', blank=True)
    menus_checked = models.TextField('菜单checked', help_text='JSON格式的字符串, 保留用户组checked内容', blank=True)
    def get_absolute_url(self):
        return reverse_lazy('easyui:GroupMenuListView')

    def __unicode__(self):
        return unicode(self.group)

    class Meta:
        verbose_name = '用户组菜单权限'
        verbose_name_plural = verbose_name


    def save(self, *args, **kwargs):
        #  把多余的menus_show中重复的ID去除
        menus_show = self.menus_show
        menu_id_set =  set(menus_show.split(','))
        self.menus_show =  ','.join(menu_id_set)

        super(GroupMenu, self).save(*args, **kwargs)
