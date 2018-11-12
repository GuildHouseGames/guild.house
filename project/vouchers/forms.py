from django import forms
from .models import GiftVoucher


class GiftVoucherFindForm(forms.Form):

    value = forms.CharField()


class GiftVoucherRedemptionForm(forms.ModelForm):

    class Meta:

        model = GiftVoucher

        fields = [
            'redeemed_by',
            'redeemed_date'
        ]

        required = [
            'redeemed_by',
            'redeemed_date'
        ]


class GiftVoucherForm(forms.ModelForm):

    class Meta:

        model = GiftVoucher

        fields = [
            'value',
            'issued_to',
            'phone',
            'email',
            'issued_date',
            'expire_date',
            'added_by',
            'is_issued',
            'notes',
        ]

        widgets = {
            'expire_date': forms.TextInput(attrs={
                'size': '10',
            }),
            'issued_date': forms.TextInput(attrs={
                'size': '10',
            }),
            'issued_to': forms.TextInput(attrs={
                'label': 'For',
                'placeholder': 'Jane & Joe Bloggs*',
            }),
            'added_by': forms.TextInput(attrs={
                'placeholder': '**',
            }),
            'notes': forms.Textarea(attrs={
            }),
            'value': forms.TextInput(attrs={
                'placeholder': '$100*',
                'size': '7',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '0400 000 000 (optional)',
                'size': '22',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'email@example.com (optional)',
                'size': '30',
            }),
        }
