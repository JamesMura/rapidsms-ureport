import datetime
import json
from django.db import connection
from django.db.models import Count
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from rapidsms_ureport.ureport.models import UreportContact


def get_date_format():
    return "%d/%m/%Y"


def get_date_from_string(start_date_string):
    return datetime.datetime.strptime(start_date_string, get_date_format()).date()


def get_ureport_contact_registrations_over_time(start_date_string, end_date_string, level):
    start_date = get_date_from_string(start_date_string)
    end_date = get_date_from_string(end_date_string)
    truncate_date = connection.ops.date_trunc_sql(level, 'autoreg_join_date')
    query = UreportContact.objects.extra({level: truncate_date})
    report = query.values(level).annotate(Count('pk')).filter(
        autoreg_join_date__range=(start_date, end_date)).order_by(level)
    out = []
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_FORMAT = '%Y-%m-%d'
    for item in report:
        count_date =""
        if type(item[level])== datetime.datetime:
            count_date = item[level].strftime(DATE_FORMAT)
        elif type(item[level])== unicode:
            count_date = datetime.datetime.strptime(item[level],DATETIME_FORMAT).strftime(DATE_FORMAT)
        else:
            count_date = ""
        out.append(
            {"date": count_date,
             "count": item['pk__count']})
    return out


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


