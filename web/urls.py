from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from ExpenseManager import views as ExpenseAppViews

urlpatterns = [
        url(r'^$', ExpenseAppViews.home, name='home'),
        url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
        url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
        url(r'^signup/$', ExpenseAppViews.signup, name='signup'),
]
