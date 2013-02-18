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
    qs = UreportContact.objects.extra({level: truncate_date})
    report = qs.values(level).annotate(Count('pk')).filter(
        autoreg_join_date__range=(start_date, end_date)).order_by(level)
    print report.query
    out = []
    for item in report:
        out.append(
            {"date": item[level].strftime("%Y-%m-%d") if type(item[level]) == datetime.datetime else "",
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


