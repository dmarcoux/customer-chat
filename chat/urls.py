from django.urls import path

from . import views

urlpatterns = [
    path("support_cases/", views.SupportCasesView.as_view(), name="support_cases"),
    path(
        "support_cases/<int:id>",
        views.SupportCaseShowView.as_view(),
        name="support_cases_show",
    ),
    path(
        "support_cases/<int:id>/messages/",
        views.SupportCaseMessagesView.as_view(),
        name="messages_create",
    ),
]
