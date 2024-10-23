from django.shortcuts import render
from ..models import SupportCase


def index(request):
    context = {
        "support_cases": SupportCase.objects.all(),
    }

    return render(request, "support_cases/index.html", context=context)


def show(request, id):
    support_case = SupportCase.objects.prefetch_related("message_set").get(pk=id)
    context = {
        "support_case": support_case,
        "messages": support_case.message_set.select_related("from_user").all(),
    }

    return render(request, "support_cases/show.html", context=context)
