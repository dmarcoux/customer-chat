import re
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from chat.models import Message, SupportCase, User


class SupportCaseShowViewTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="customer123", password="superpass")
        self.otherUser = User.objects.create_user(username="otherCustomer", password="superpass")
        self.staffUser = User.objects.create_user(username="customerAgent123", password="superpass", is_staff=True)

        self.support_case = SupportCase.objects.create(from_user=self.user)
        self.message = Message.objects.create(
            support_case=self.support_case,
            from_user=self.user,
            content="Hello, I need help with my computer.",
        )

    def test_user_cannot_access_support_case_of_another_user(self) -> None:
        self.client.force_login(self.otherUser)

        response = self.client.get(reverse("support_cases_show", kwargs={"pk": self.support_case.id}))

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_user_can_access_their_support_case(self) -> None:
        self.client.force_login(self.user)

        response = self.client.get(reverse("support_cases_show", kwargs={"pk": self.support_case.id}))

        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert re.search(r"Support Case #[\d]+", html_content)
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        assert self.message.content in html_content

    def test_staff_user_can_access_support_case(self) -> None:
        self.client.force_login(self.staffUser)

        response = self.client.get(reverse("support_cases_show", kwargs={"pk": self.support_case.id}))

        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert re.search(r"Support Case #[\d]+", html_content)
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        assert self.message.content in html_content

    def test_404_when_support_case_does_not_exist(self) -> None:
        self.client.force_login(self.user)

        response = self.client.get(reverse("support_cases_show", kwargs={"pk": 999_999_999}))

        assert response.status_code == HTTPStatus.NOT_FOUND
