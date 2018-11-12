# -*- coding: utf-8 -*-
from . import views
from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required

PERMISSION_REQUIRED = 'vouchers.change_giftvoucher'

urls = [

    url(
        r'^$',
        permission_required(PERMISSION_REQUIRED)(
            views.GiftVoucherListView.as_view()
        ),
        name='voucher_list'
    ),

    url(
        r'^find/$',
        permission_required(PERMISSION_REQUIRED)(
            views.GiftVoucherFindView.as_view()
        ),
        name='voucher_find'
    ),

    url(
        r'^find/not/$',
        permission_required(PERMISSION_REQUIRED)(
            views.GiftVoucherNotFindView.as_view()
        ),
        name='voucher_find_not'
    ),

    url(
        r'^add/$',
        permission_required(PERMISSION_REQUIRED)(
            views.GiftVoucherCreateView.as_view()
        ),
        name='voucher_add'
    ),

    url(
        r'^(?P<number>[\w-]+)/$',
        permission_required(PERMISSION_REQUIRED)(
            views.GiftVoucherDetailView.as_view()
        ),
        name='voucher_detail'
    ),

    url(
        r'^(?P<number>[\w-]+)/redeem/$',
        permission_required(PERMISSION_REQUIRED)(
            views.GiftVoucherUpdateView.as_view()
        ),
        name='voucher_update'
    ),

]

urlpatterns = [url(r'^', include(urls, namespace='vouchers'))]
