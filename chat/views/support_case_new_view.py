from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from chat.forms import MessageForm


class SupportCaseNewView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_staff:
            raise PermissionDenied

        context = {"message_form": MessageForm()}

        return render(request, "support_cases/new.html", context=context)
