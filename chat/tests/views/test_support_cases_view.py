from http import HTTPStatus

from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse

from chat.models import Message, SupportCase, User


class SupportCasesViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="customer123", password="superpass")
        self.otherUser = User.objects.create_user(username="otherCustomer", password="superpass")
        self.staffUser = User.objects.create_user(username="customerAgent123", password="superpass", is_staff=True)

        self.supportCaseUser1 = SupportCase.objects.create(from_user=self.user)
        self.supportCaseUser2 = SupportCase.objects.create(from_user=self.user)
        self.supportCaseOtherUser = SupportCase.objects.create(from_user=self.otherUser)

    def test_get_show_all_support_cases_for_staff(self) -> None:
        self.client.force_login(self.staffUser)

        response = self.client.get(reverse("support_cases"))
        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert "Open a support case" not in html_content

        support_cases = [
            self.supportCaseUser1,
            self.supportCaseUser2,
            self.supportCaseOtherUser,
        ]
        for support_case in support_cases:
            link_url = reverse("support_cases_show", kwargs={"pk": support_case.id})
            self.assertInHTML(
                f'<a href="{link_url}">Support Case #{support_case.id}</a>',
                html_content,
            )

    def test_get_show_support_cases_only_for_user(self) -> None:
        self.client.force_login(self.user)

        response = self.client.get(reverse("support_cases"))
        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert "Open a support case" in html_content

        support_cases = [self.supportCaseUser1, self.supportCaseUser2]
        for support_case in support_cases:
            link_url = reverse("support_cases_show", kwargs={"pk": support_case.id})
            self.assertInHTML(
                f'<a href="{link_url}">Support Case #{support_case.id}</a>',
                html_content,
            )

        link_url = reverse("support_cases_show", kwargs={"pk": self.supportCaseOtherUser.id})
        self.assertNotInHTML(
            f'<a href="{link_url}">Support Case #{self.supportCaseOtherUser.id}</a>',
            html_content,
        )

    def test_post_user_staff_unauthorized_to_open_support_case(self) -> None:
        self.client.force_login(self.staffUser)

        response = self.client.post(reverse("support_cases"), data={"content": "Hello!"})

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_post_user_can_open_support_case(self) -> None:
        self.client.force_login(self.user)

        initial_support_cases_count = SupportCase.objects.count()

        message = "Hello! I need your help with my bike."
        response = self.client.post(
            reverse("support_cases"),
            data={"content": message},
        )

        support_case = SupportCase.objects.last()

        self.assertRedirects(response, reverse("support_cases_show", kwargs={"pk": support_case.id}))
        assert SupportCase.objects.count() == initial_support_cases_count + 1
        assert model_to_dict(support_case, exclude=["id"]) == {"from_user": self.user.id}
        assert model_to_dict(Message.objects.last(), exclude=["id"]) == {
            "content": message,
            "from_user": self.user.id,
            "support_case": support_case.id,
        }

    def test_post_user_cannot_open_support_case_when_message_is_empty(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(reverse("support_cases"), data={"content": ""})

        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert "Your support case could not be opened. Try again." in html_content
