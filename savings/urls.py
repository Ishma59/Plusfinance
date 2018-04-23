from django.conf.urls import url
from savings.views import *

urlpatterns = [
    # Client Savings
    url(r'^client/(?P<client_id>\d+)/savings/application/$', client_savings_application_view, name='clientsavingsapplication'),
    url(r'^client/(?P<client_id>\d+)/savings/account/view/$', client_savings_account_view, name='clientsavingsaccount'),
    url(r'^client/(?P<client_id>\d+)/savings/deposits/list/$', client_savings_deposits_list_view, name='listofclientsavingsdeposits'),
    url(r'^client/(?P<client_id>\d+)/savings/withdrawals/list/$', client_savings_withdrawals_list_view, name='listofclientsavingswithdrawals'),

    # Group Savings
    url(r'^group/(?P<group_id>\d+)/savings/application/$', group_savings_application_view, name='groupsavingsapplication'),
    url(r'^group/(?P<group_id>\d+)/savings/account/view/$', group_savings_account_view, name='groupsavingsaccount'),
    url(r'^group/(?P<group_id>\d+)/savings/deposits/list/$', group_savings_deposits_list_view, name='viewgroupsavingsdeposits'),
    url(r'^group/(?P<group_id>\d+)/savings/withdrawals/list/$', group_savings_withdrawals_list_view, name='viewgroupsavingswithdrawals'),

    # Change Savings Account Status
    url(r'^savings/account/(?P<savingsaccount_id>\d+)/change-status/$', change_savings_account_status,
        name='change-savings-account-status'),
]
