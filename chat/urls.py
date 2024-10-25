from django.urls import path

from . import views

urlpatterns = [
    path("", views.SupportCasesView.as_view(), name="support_cases"),
    path(
        "new/",
        views.SupportCaseNewView.as_view(),
        name="support_cases_new",
    ),
    path(
        "<int:id>/",
        views.SupportCaseShowView.as_view(),
        name="support_cases_show",
    ),
    path(
        "<int:id>/messages/",
        views.SupportCaseMessagesView.as_view(),
        name="messages_create",
    ),
]
