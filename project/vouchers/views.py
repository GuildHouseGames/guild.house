from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import (
    GiftVoucherForm, GiftVoucherRedemptionForm, GiftVoucherFindForm)
from .models import GiftVoucher


class GiftVoucherListView(generic.ListView):

    model = GiftVoucher

    def get_queryset(self):
        return super(GiftVoucherListView,
                     self).get_queryset().order_by('-issued_date')


class GiftVoucherFindView(generic.FormView):

    form_class = GiftVoucherFindForm

    template_name = 'vouchers/voucher_find.html'

    def form_valid(self, form):
        gv = GiftVoucher.objects.filter(number=form.cleaned_data.get('value'))
        if gv:
            return HttpResponseRedirect(gv[0].get_absolute_url())
        else:
            return HttpResponseRedirect('/vouchers/find/not/')
        return super(GiftVoucherFindView, self).form_valid(form)


class GiftVoucherNotFindView(GiftVoucherFindView):

    template_name = 'vouchers/voucher_find_not.html'


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
