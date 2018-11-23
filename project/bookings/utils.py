# -*- coding: utf-8 -*-
from datetime import date, time, datetime, timedelta

from django.db.models import Max
from django.utils.timezone import make_aware

from .models import Booking
from .settings import DEFAULT_BOOKING_DURATION, UNKNOWN_EMAIL, SERVICE_CHOICE

# Synchronising scrape from Revel to bookings system.
# To be automated daily.


def import_revel_bookings(scrape):

    # Utility functions

    def create_date_from_string(d):
        day, month, year = [int(x) for x in d.split("/")]
        return datetime(year, month, day, 0, 0, 0)

    def create_time_from_string(t):
        hour, minute = [int(x) for x in t.split(":")]
        return time(hour, minute)

    def create_legacy_code(data):
        return "".join(data[0:-1]).replace(" ", "")

    def map_status(data):
        mapping = {
            'Reserved': 'booked',
            'No Show': 'no_show'
        }
        return mapping[data]

    # Confident that they'll do an update one day that will break this.
    # -> Happened Aug 2017

    split_string_start = "Reserved On\nReserved For\nOrder ID\nStatus\nParty Size\nWait time\nCustomer\nPhone\nNotes & Preferences\n"
    split_string_end = "Watch the tutorial"

    data_raw = scrape.split(split_string_start)[-1].split(split_string_end)
    data_list = [x.split("\t") for x in data_raw[0].split("\n")]

    # Mapping is as follows:
    """

    # 0 Reserved On
    # 1 Reserved For
    # 2 Order ID
    # 3 Status
    # 4 Party Size
    # 5 Wait time
    # 6 Customer
    # 7 Phone
    # 8 Notes & Preferences

    0 updated_at
    1 reserved_date, reserved_time
    2 -
    3 status
    4 party_size
    5 -
    6 name
    7 phone
    8 note
    legacy_code
    """

    success = []
    for data in data_list:
        if not len(data) == 9:
            continue

        reserve_date = data[1].split(" ")[0]
        reserve_time = data[1].split(" ")[1]
        check_kwargs = {
            'reserved_date': create_date_from_string(reserve_date),
            'reserved_time': create_time_from_string(reserve_time),
            'name': data[6],
            'phone': data[7],
            'party_size': int(data[4]),
        }

        kwargs = {
            'created_at': make_aware(create_date_from_string(data[0])),
            'status': map_status(data[3]),
            'notes': data[8],
            'legacy_code': create_legacy_code(data),
            'duration': DEFAULT_BOOKING_DURATION,
            'email': UNKNOWN_EMAIL,
        }

        obj, is_created = Booking.objects.get_or_create(**check_kwargs)
        obj.__dict__.update(**kwargs)
        obj.save()
        if is_created:
            success.append((obj, '** new! **: '))
        else:
            success.append((obj, 'existing: '))
    return success
