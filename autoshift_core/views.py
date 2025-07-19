from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .mainframe import run_command
from .splunk import SplunkHECClient

import asyncio


@require_POST
@csrf_exempt
async def run_automation(request):
    command = request.POST.get("command")
    if not command:
        return HttpResponseBadRequest("'command' parameter required")

    output = run_command(command.split())

    if settings.SPLUNK_HEC_URL and settings.SPLUNK_HEC_TOKEN:
        client = SplunkHECClient(settings.SPLUNK_HEC_URL, settings.SPLUNK_HEC_TOKEN)
        await client.send_event({"command": command, "output": output})

    return JsonResponse({"output": output})
