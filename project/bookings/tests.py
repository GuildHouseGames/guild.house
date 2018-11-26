# -*- coding: utf-8 -*-
#from django.test import TestCase
from unittest import TestCase
from datetime import timedelta

from .models import get_duration


class TestGetDuration(TestCase):

    def test_get_duration_1(self):
        self.assertEqual(get_duration(1), timedelta(minutes=60))

    def test_get_duration_2(self):
        self.assertEqual(get_duration(2), timedelta(minutes=90))

    def test_get_duration_3(self):
        self.assertEqual(get_duration(3), timedelta(minutes=120))

    def test_get_duration_4(self):
        self.assertEqual(get_duration(4), timedelta(minutes=150))

    def test_get_duration_5(self):
        self.assertEqual(get_duration(5), timedelta(hours=3))

    def test_get_duration_8(self):
        self.assertEqual(get_duration(8), timedelta(hours=4))

    def test_get_duration_20(self):
        self.assertEqual(get_duration(20), timedelta(hours=4))


"""
from .forms import AUPhoneNumberField

# Test:

AUPhoneNumberField.clean()

# n8_pass = "12345678"
# n8_fail = "abc45678"
# n10_pass = "0123456789"
# n10_fail = "1234567890"


# Successful scrape:
"""

#scrape = """Skip to navigation\r\nSkip to content\r\nSkip to sidebar\r\n\r\n \r\nelena@guild.house\r\n \r\n•••••••••••••••\r\nWelcome, elena@guild.house\r\nEstablishment(s): Guild\r\nEn\r\n Billing About Need Help? Change Password Logout \r\n3Offline Stations 27/05/2017, 10:49:14\r\nOverview\r\n \r\nReports\r\n \r\nProducts\r\n \r\nInventory\r\n \r\nEmployees\r\n \r\nSchedules\r\n \r\nAppointments\r\n \r\nCRM\r\n \r\nEstablishment\r\n \r\nSettings\r\nSales Summary\r\nOperations\r\nHourly Sales\r\nProduct Mix\r\nOrder History\r\nPayment Summary\r\nOther Reports\r\nReservations\r\n(27/05/2017 03:00 - 28/05/2017 03:00)\t\r\n \r\nSearch customer\r\n \r\n Filter by Reserved On\r\n.\r\nPrint Report\r\nReserved On\tReserved For\tOrder ID\tStatus\tParty Size\tWait time\tCustomer\tPhone\tNotes & Preferences\r\n18/05/2017\t27/05/2017 19:30 \t\tReserved\t4\t\tJoanne\t0434852218\t\r\n19/05/2017\t27/05/2017 18:00 \t\tReserved\t7\t\tHeidi\t0409091365\t\r\n24/05/2017\t27/05/2017 18:30 \t\tReserved\t10\t\tHeidi\t0404945471\t\r\n26/05/2017\t27/05/2017 18:30 \t\tReserved\t7\t\tElizabeth\t0431954379\tTokaido\r\n26/05/2017\t27/05/2017 18:00 \t\tReserved\t8\t\tPeter Lee\t0405148225\t\r\n17/05/2017\t27/05/2017 12:00 \t\tReserved\t8\t\tClift\t0404690273\t15th bday\r\n22/05/2017\t27/05/2017 18:30 \t\tReserved\t4\t\tSarah\t0423145996\t\r\n26/05/2017\t27/05/2017 17:15 \t\tReserved\t10\t\tKelly\t0414584518\t\r\n22/05/2017\t27/05/2017 17:00 \t\tReserved\t8\t\tHelen Jennings\t0419987955\t\r\n26/05/2017\t27/05/2017 18:30 \t\tReserved\t2\t\tBryce\t0459840181\t\r\n26/05/2017\t27/05/2017 18:00 \t\tReserved\t5\t\tNathan\t0410414231\tinside\r\n26/05/2017\t27/05/2017 13:00 \t\tReserved\t2\t\tBowman\t\t0400753609\r\n15/05/2017\t27/05/2017 12:30 \t\tReserved\t4\t\tLaura\t0402576442\t\r\nWatch the tutorial""" # noqa
