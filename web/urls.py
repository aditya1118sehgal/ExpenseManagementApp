from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from ExpenseManager import views as ExpenseAppViews

urlpatterns = [
        url(r'^$', ExpenseAppViews.home, name='home'),
        url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
        url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
        url(r'^signup/$', ExpenseAppViews.signup, name='signup'),
        url(r'^expense/new/$', ExpenseAppViews.expense_new, name='expense_new'),
        url(r'^expense/(?P<pk>\d+)/$', ExpenseAppViews.expense_detail, name='expense_detail'),
        url(r'^expense/(?P<pk>\d+)/edit/$', ExpenseAppViews.expense_edit, name='expense_edit'),
        url(r'^expense/(?P<pk>\d+)/delete/$', ExpenseAppViews.expense_delete, name='expense_delete'),
        url(r'^report/$', ExpenseAppViews.report, name='report')
]
