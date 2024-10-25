from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import View
from ..forms import MessageForm


class SupportCaseNewView(View):
    def get(self, request):
        if request.user.is_staff:
            raise PermissionDenied

        context = {"message_form": MessageForm()}

        return render(request, "support_cases/new.html", context=context)
