import logging
from django.shortcuts import render
from django.http import JsonResponse
from .queries import get_team_records

logger = logging.getLogger(__name__)

def index_view(request):
    return render(request, 'base.html')

def team_records_api(request):
    records = get_team_records()
    return JsonResponse(list(records.values()), safe=False)
