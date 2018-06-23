# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import TemporaryMember, Member, Membership, MembershipTag, Payment


admin.site.register(TemporaryMember)


class MembershipInline(admin.TabularInline):

    model = Membership


class PaymentInline(admin.TabularInline):

    model = Payment


class MemberAdmin(admin.ModelAdmin):

    list_display = ['number', 'name', 'sort_name', 'ref_name']
    search_fields = ['number', 'name', 'sort_name', 'ref_name']
    model = Member
    inlines = [
        MembershipInline,
        PaymentInline
    ]


admin.site.register(Member, MemberAdmin)


class MembershipTagInline(admin.TabularInline):

    model = MembershipTag


class MembershipAdmin(admin.ModelAdmin):

    model = Membership
    inlines = [MembershipTagInline]


admin.site.register(Membership, MembershipAdmin)
