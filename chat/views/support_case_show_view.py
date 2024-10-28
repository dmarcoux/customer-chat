from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from chat.forms import MessageForm
from chat.models import SupportCase


class SupportCaseShowView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        support_case = get_object_or_404(SupportCase.objects.prefetch_related("message_set"), pk=pk)

        if not request.user.is_staff and request.user.id != support_case.from_user_id:
            # Responding with a 404 just like if the support case didn't exist.
            # Users don't have to know this support case exists if they aren't authorized to see it.
            exception_message = "No SupportCase matches the given query."
            raise Http404(exception_message)

        context = {
            "support_case": support_case,
            "support_case_messages": support_case.message_set.select_related("from_user").all(),
            "message_form": MessageForm(),
        }

        return render(request, "support_cases/show.html", context=context)
