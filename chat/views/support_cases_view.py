from django.shortcuts import render
from django.views import View
from ..models import SupportCase


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
