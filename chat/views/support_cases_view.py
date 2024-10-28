from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View

from chat.forms import MessageForm
from chat.models import SupportCase


class SupportCasesView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        support_cases = (
            SupportCase.objects.all()
            if request.user.is_staff
            else SupportCase.objects.filter(from_user_id__exact=request.user.id)
        )

        context = {
            "support_cases": support_cases,
        }

        return render(request, "support_cases/index.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if request.user.is_staff:
            raise PermissionDenied

        form = MessageForm(request.POST)

        if form.is_valid():
            support_case = SupportCase(from_user=request.user)
            support_case.save()
            form.create_message(support_case, support_case.from_user)

            return redirect("support_cases_show", pk=support_case.id)

        context = {
            "message_form": form,
        }

        # This only happens if the user somehow tinkered with the request
        messages.error(request, "Your support case could not be opened. Try again.")

        return render(request, "support_cases/new.html", context=context)
