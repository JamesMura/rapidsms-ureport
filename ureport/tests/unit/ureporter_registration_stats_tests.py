import datetime
from django.core.exceptions import FieldError
from django.test import TestCase
from rapidsms_ureport.ureport import ureport_stats_views
from rapidsms_ureport.ureport.models import UreportContact
from rapidsms_ureport.ureport.ureport_stats_views import get_date_from_string, get_ureport_contact_registrations_over_time


def create_ureporter_by_registration_date(date):
    return UreportContact(autoreg_join_date=get_date_from_string(date),
                          quit_date=get_date_from_string('13/1/2017'), responses=0,
                          questions=0, age=19, incoming=0, connection_pk=0, reporting_location_id=0, user_id=0).save()


def create_ureporter_with_district():
    return UreportContact(district="Kampala", autoreg_join_date=get_date_from_string("5/1/2011"),
                          quit_date=get_date_from_string('13/1/2017'), responses=0,
                          questions=0, age=19, incoming=0, connection_pk=0, reporting_location_id=0, user_id=0).save()


def create_ureporter_with_gender(gender):
    return UreportContact(district="Kampala", autoreg_join_date=get_date_from_string("5/1/2011"),
                          quit_date=get_date_from_string('13/1/2017'), responses=0,
                          questions=0, age=12, incoming=0, connection_pk=0, reporting_location_id=0, user_id=0,
                          gender=gender).save()


class UreportRegistrationStatsHelpersTest(TestCase):
    def test_can_convert_from_string_to_datetime(self):
        self.assertEquals(get_date_from_string('5/1/2011'), datetime.date(day=5, month=1, year=2011))


# class UreporterRegistrationStatsTest(TestCase):
#     def setUp(self):
#         create_ureporter_by_registration_date('5/1/2011')
#         create_ureporter_by_registration_date('7/1/2011')
#         create_ureporter_by_registration_date('8/3/2011')
#         create_ureporter_by_registration_date('8/3/2011')
#         create_ureporter_by_registration_date('8/3/2011')
#
#
#     def test_can_list_counts_per_month(self):
#         self.assertEquals([{'count': 2, 'date': "2011-01-01"}, {'count': 3, 'date': "2011-03-01"}],
#                           get_ureport_contact_registrations_over_time('1/1/2011', '1/4/2011', 'month'))


class UreportContactWithMissingDistrictTest(TestCase):
    def setUp(self):
        create_ureporter_by_registration_date('5/1/2011')
        create_ureporter_by_registration_date('7/1/2011')
        create_ureporter_with_district()

    def test_can_count_ureport_contacts_with_missing_district(self):
        self.assertEquals({"count": 2, "percentage": 200 / 3},
                          ureport_stats_views.get_all_ureport_contacts_missing_field('district'))

    def test_that_throws_exception_when_field_is_wrong(self):
        with self.assertRaises(FieldError):
            ureport_stats_views.get_all_ureport_contacts_missing_field('districts')


class UreportContactWithMissingAgeTest(TestCase):
    def setUp(self):
        create_ureporter_by_registration_date('5/1/2011')

    def test_can_count_ureport_contacts_with__missing_age(self):
        self.assertEquals({"count": 0, "percentage": 0},
                          ureport_stats_views.get_all_ureport_contacts_missing_numeric_field('age'))

    def test_that_throws_exception_when_field_is_wrong(self):
        with self.assertRaises(FieldError):
            ureport_stats_views.get_all_ureport_contacts_missing_numeric_field('ages')


class UreportContactWithMissingGenderTest(TestCase):
    def setUp(self):
        create_ureporter_by_registration_date('5/1/2011')
        create_ureporter_by_registration_date('5/1/2011')
        create_ureporter_with_gender("male")

    def test_blank_genders_are_counted(self):
        create_ureporter_with_gender("")
        self.assertEquals({"count": 3, "percentage": 300 / 4},
                          ureport_stats_views.get_all_ureport_contacts_missing_field('gender'))

    def test_can_count_ureport_contacts_with__missing_gender(self):
        self.assertEquals({"count": 2, "percentage": 200 / 3},
                          ureport_stats_views.get_all_ureport_contacts_missing_field('gender'))

    def test_that_throws_exception_when_field_name_is_wrong(self):
        with self.assertRaises(FieldError):
            ureport_stats_views.get_all_ureport_contacts_missing_field('Gender')
            ureport_stats_views.get_all_ureport_contacts_missing_field('Genders')


class UreportContactWithMissingVillageTest(TestCase):
    def setUp(self):
        create_ureporter_by_registration_date('5/1/2011')
        create_ureporter_by_registration_date('5/1/2011')
        create_ureporter_with_gender("male")

    def test_can_count_ureport_contacts_with__missing_village(self):
        self.assertEquals({"count": 3, "percentage": 100},
                          ureport_stats_views.get_all_ureport_contacts_missing_field('village'))

    def test_that_throws_exception_when_field_name_is_wrong(self):
        with self.assertRaises(FieldError):
            ureport_stats_views.get_all_ureport_contacts_missing_field('villageeeg')