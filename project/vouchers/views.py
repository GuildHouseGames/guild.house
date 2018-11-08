from datetime import date, timedelta
from django import forms
from django.views import generic
from .forms import GiftVoucherForm, GiftVoucherRedemptionForm
from .models import GiftVoucher


class GiftVoucherListView(generic.ListView):

    model = GiftVoucher

    def get_queryset(self):
        return super(GiftVoucherListView,
                     self).get_queryset().order_by('-issued_date')


class GiftVoucherDetailView(generic.DetailView):

    model = GiftVoucher

    slug_field = 'number'

    slug_url_kwarg = 'number'


class GiftVoucherCreateView(generic.edit.CreateView):

    template_name = 'vouchers/giftvoucher_form.html'

    form_class = GiftVoucherForm

    def get_initial(self):
        return {
            'issued_date': date.today(),
            'expire_date': date.today() + timedelta(days=366),
        }


class GiftVoucherUpdateView(generic.edit.UpdateView):

    model = GiftVoucher

    form_class = GiftVoucherRedemptionForm

    slug_field = 'number'

    slug_url_kwarg = 'number'

    template_name = 'vouchers/giftvoucher_detail.html'

    def get_initial(self):
        return {
            'redeemed_date': date.today(),
        }
