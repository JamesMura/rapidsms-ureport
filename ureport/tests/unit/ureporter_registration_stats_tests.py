import datetime
from django.test import TestCase
from rapidsms_ureport.ureport.models import UreportContact
from rapidsms_ureport.ureport.ureport_stats_views import get_date_from_string, get_ureport_contact_registrations_over_time


def create_ureporter_by_registration_date(date):
    return UreportContact(autoreg_join_date=get_date_from_string(date),
                          quit_date=get_date_from_string('13/1/2017'), responses=0,
                          questions=0, age=19, incoming=0, connection_pk=0, reporting_location_id=0, user_id=0).save()


class UreportRegistrationStatsHelpersTest(TestCase):
    def test_can_convert_from_string_to_datetime(self):
        self.assertEquals(get_date_from_string('5/1/2011'), datetime.date(day=5, month=1, year=2011))


class UreporterRegistrationStatsTest(TestCase):
    def setUp(self):
        create_ureporter_by_registration_date('5/1/2011')
        create_ureporter_by_registration_date('7/1/2011')
        create_ureporter_by_registration_date('8/3/2011')
        create_ureporter_by_registration_date('8/3/2011')
        create_ureporter_by_registration_date('8/3/2011')


    def test_can_list_counts_per_month(self):
        self.assertEquals([{'count': 2, 'date': "2011-02-01"},{'count': 3, 'date': "2011-03-01"}],
                          get_ureport_contact_registrations_over_time('1/1/2011', '1/4/2011', 'month'))