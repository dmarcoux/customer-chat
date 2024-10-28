import re
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from chat.models import SupportCase, User


class SupportCaseMessagesViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="customer123", password="superpass")
        self.otherUser = User.objects.create_user(username="otherCustomer", password="superpass")
        self.staffUser = User.objects.create_user(username="customerAgent123", password="superpass", is_staff=True)

        self.support_case = SupportCase.objects.create(from_user=self.user)

    def test_user_cannot_send_message_to_inexistent_support_case(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("messages_create", kwargs={"pk": 999_999_999}),
            data={"content": "Something something 123"},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_user_cannot_send_message_to_support_case_from_other_user(self) -> None:
        self.client.force_login(self.otherUser)

        response = self.client.post(
            reverse("messages_create", kwargs={"pk": self.support_case.id}),
            data={"content": "Wow, this is really helpful!"},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_user_can_send_message_to_their_support_case(self) -> None:
        self.client.force_login(self.user)

        message = "Hello, could you help me with my computer?"
        response = self.client.post(
            reverse("messages_create", kwargs={"pk": self.support_case.id}),
            data={"content": message},
            follow=True,
        )
        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert re.search(r"Support Case #[\d]+", html_content)
        assert "Your message was added to the support case." in html_content
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        assert message in html_content

    def test_staff_user_can_send_message_to_any_support_case(self) -> None:
        self.client.force_login(self.staffUser)

        message = "Hello, I am here to help you."
        response = self.client.post(
            reverse("messages_create", kwargs={"pk": self.support_case.id}),
            data={"content": message},
            follow=True,
        )
        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert re.search(r"Support Case #[\d]+", html_content)
        assert "Your message was added to the support case." in html_content
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        assert message in html_content

    def test_user_cannot_send_empty_message(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("messages_create", kwargs={"pk": self.support_case.id}),
            data={"content": ""},
        )

        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        assert "Your message was added to the support case." not in html_content
