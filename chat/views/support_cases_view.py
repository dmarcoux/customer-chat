from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View
from ..models import SupportCase
from ..forms import MessageForm


class SupportCasesView(View):
    def get(self, request):
        support_cases = (
            SupportCase.objects.all()
            if request.user.is_staff
            else SupportCase.objects.filter(from_user_id__exact=request.user.id)
        )

        context = {
            "support_cases": support_cases,
        }

        return render(request, "support_cases/index.html", context=context)

    def post(self, request):
        if request.user.is_staff:
            raise PermissionDenied

        form = MessageForm(request.POST)

        if form.is_valid():
            support_case = SupportCase(from_user=request.user)
            support_case.save()
            form.create_message(request, support_case, support_case.from_user)

            return redirect("support_cases_show", id=support_case.id)
        else:
            context = {
                "message_form": form,
            }

            return render(request, "support_cases/show.html", context=context)
