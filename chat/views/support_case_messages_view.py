from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ..models import SupportCase
from ..forms import MessageForm


class SupportCaseMessagesView(View):
    def post(self, request, id):
        form = MessageForm(request.POST)

        support_case = get_object_or_404(
            SupportCase.objects.prefetch_related("message_set"), pk=id
        )

        if not request.user.is_staff and request.user.id != support_case.from_user_id:
            # Responding with a 404 just like if the support case didn't exist.
            # Users don't have to know this support case exists if they aren't authorized to see it.
            raise Http404("No SupportCase matches the given query.")

        if form.is_valid():
            form.create_message(support_case, request.user)
            messages.success(request, "Your message was added to the support case.")

            return redirect("support_cases_show", id=id)

        context = {
            "support_case": support_case,
            "support_case_messages": support_case.message_set.select_related(
                "from_user"
            ).all(),
            "message_form": form,
        }

        return render(request, "support_cases/show.html", context=context)
