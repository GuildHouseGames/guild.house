from datetime import date, timedelta
from django.db import models
from django.shortcuts import reverse
from project.rolodex.models import Email, Phone


class GiftVoucher(models.Model):

    is_valid = models.BooleanField(default=True)

    is_legacy = models.BooleanField(default=True)

    number = models.IntegerField(unique=True)

    value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    is_issued = models.BooleanField(default=True)

    issued_to = models.CharField(
        max_length=128,
        null=True, blank=True, default='',
    )

    issued_date = models.DateField(
        # auto_now_add=True,
    )

    redeemed_by = models.CharField(
        max_length=64,
        null=True, blank=True, default='',
    )

    redeemed_date = models.DateField(
        null=True, blank=True
    )

    expire_date = models.DateField()

    added_by = models.CharField(
        max_length=64,
    )

    user = models.ForeignKey(
        'auth.User',
        models.PROTECT,
        default=1,
    )

    email = models.EmailField(
        null=True, blank=True
    )

    phone = models.CharField(
        max_length=16,
        null=True, blank=True
    )

    notes = models.CharField(
        max_length=512,
        null=True, blank=True, default='',
    )

    class Meta:
        ordering = ['number']

    @property
    def is_expired(self):
        if self.expire_date < date.today() + timedelta(days=1):
            if self.is_valid:
                self.is_valid = False
                self.save()
            return True
        if self.redeemed_date or self.redeemed_by:
            return True
        return False

    def get_absolute_url(self):
        return reverse('vouchers:voucher_detail',
                       kwargs={'number': self.number})

    @classmethod
    def get_number(cls):
        return cls.objects.aggregate(models.Max('number'))['number__max']+1

    def save(self, *args, **kwargs):

        if not self.number:
            self.number = self.get_number()

        if not self.expire_date:
            self.expires_date = self.date_issued+timedelta(days=366)

        if self.email:
            Email.objects.get_or_create(email=self.email)

        if self.phone:
            Phone.objects.get_or_create(phone=self.phone)

        return super(GiftVoucher, self).save(*args, **kwargs)
