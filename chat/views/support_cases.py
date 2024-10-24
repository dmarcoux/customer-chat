from django.http import Http404
from django.shortcuts import render, get_object_or_404
from ..models import SupportCase


def index(request):
    support_cases = (
        SupportCase.objects.all()
        if request.user.is_staff
        else SupportCase.objects.filter(from_user_id__exact=request.user.id)
    )

    context = {
        "support_cases": support_cases,
    }

    return render(request, "support_cases/index.html", context=context)


def show(request, id):
    support_case = get_object_or_404(
        SupportCase.objects.prefetch_related("message_set"), pk=id
    )

    if not request.user.is_staff and request.user.id != support_case.from_user_id:
        # Responding with a 404 just like if the support case didn't exist.
        # Users don't have to know this support case exists if they aren't authorized to see it.
        raise Http404("No SupportCase matches the given query.")

    context = {
        "support_case": support_case,
        "support_case_messages": support_case.message_set.select_related(
            "from_user"
        ).all(),
    }

    return render(request, "support_cases/show.html", context=context)
