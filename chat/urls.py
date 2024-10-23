from django.urls import path

from . import views

urlpatterns = [
    path("support_cases/", views.support_cases.index, name="index"),
    path("support_cases/<int:id>", views.support_cases.show, name="show"),
]
