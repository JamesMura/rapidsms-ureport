#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from ureport.models import AutoregGroupRules
from ureport.forms import GroupRules
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from generic.sorters import SimpleSorter
from generic.views import generic




def view_autoreg_rules(request):
    columns = [('Group', True, 'group__name', SimpleSorter(),),('Rule', True, 'rule', SimpleSorter(),),('Words', True, 'words', SimpleSorter(),)]
    qs=AutoregGroupRules.objects.all()
    return generic(
        request,
        model=AutoregGroupRules,
        queryset=qs,   
        objects_per_page=20,
        results_title='Group Rules',
        selectable=False,
        partial_row='ureport/partials/group_row.html',
        base_template='ureport/group_base.html',
        columns=columns,
        
    )


@login_required
def set_autoreg_rules(request):
    if request.GET.get('gr', None):
        g = Group.objects.get(pk=request.GET.get('gr'))

        try:
            a_g = AutoregGroupRules.objects.get(group=g)
            return HttpResponse(str(a_g.values))
        except AutoregGroupRules.DoesNotExist:
            return HttpResponse('')

    if request.method == 'POST':

        group_form = GroupRules(request.POST)
        if group_form.is_valid():
            group_form.save()
    else:
        group_form = GroupRules()
    return render_to_response('ureport/partials/groups_form.html',
                              {'group_form': group_form},
                              context_instance=RequestContext(request))


