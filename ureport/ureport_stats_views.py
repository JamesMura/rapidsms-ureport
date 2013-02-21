import datetime
import json
from django.db import connection
from django.db.models import Count, Q
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from rapidsms_ureport.ureport.models import UreportContact


def get_date_from_string(start_date_string):
    return datetime.datetime.strptime(start_date_string, "%d/%m/%Y").date()


def get_ureport_contact_registrations_over_time(start_date_string, end_date_string, level):
    start_date = get_date_from_string(start_date_string)
    end_date = get_date_from_string(end_date_string)
    truncate_date = connection.ops.date_trunc_sql(level, 'autoreg_join_date')
    query = UreportContact.objects.extra({level: truncate_date})
    report = query.values(level).annotate(Count('pk')).filter(
        autoreg_join_date__range=(start_date, end_date)).order_by(level)
    DATE_FORMAT = '%Y-%m-%d'
    return [{'date': item[level].strftime(DATE_FORMAT) if item[level] else "", 'count': item['pk__count']} for item in
            report]


class UreporterRegistrationOverTimeJSONVIew(View):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        counts = get_ureport_contact_registrations_over_time(start_date, end_date, 'day')
        return HttpResponse(json.dumps(counts), content_type="application/json")


class UreporterRegistrationOverTimeView(TemplateResponseMixin, View):
    template_name = "spikes/ureport_registration.html"

    def get(self, request):
        return self.render_to_response({})


class UreportContactMissingFieldJSONView(View):
    def get(self, request):
        field = self.request.GET.get('field')
        data = []
        if field in ["age"]:
            data = get_all_ureport_contacts_missing_numeric_field(field)
        else:
            data = get_all_ureport_contacts_missing_field(field)
        return HttpResponse(json.dumps(data), content_type="application/json")


def get_all_ureport_contacts_missing_field(field_name):
    total_number_of_reporters = UreportContact.objects.count()
    queryset = UreportContact.objects.filter(
        Q(**{'{0}__{1}'.format(field_name, "isnull"): True}) | Q(**{field_name: ""}))

    number_contacts_without_field = queryset.aggregate(Count('pk'))['pk__count']
    print queryset.query
    return {"count": number_contacts_without_field,
            "percentage": (number_contacts_without_field * 100 / total_number_of_reporters)}


def get_all_ureport_contacts_missing_numeric_field(field_name):
    total_number_of_reporters = UreportContact.objects.count()
    queryset = UreportContact.objects.filter(
        **{'{0}__{1}'.format(field_name, "isnull"): True})
    number_contacts_without_field = queryset.aggregate(Count('pk'))['pk__count']
    print queryset.query
    return {"count": number_contacts_without_field,
            "percentage": (number_contacts_without_field * 100 / total_number_of_reporters)}