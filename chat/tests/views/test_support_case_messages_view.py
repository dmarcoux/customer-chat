from django.test import TestCase
from django.urls import reverse
from ...models import User, SupportCase
from http import HTTPStatus


class SupportCaseMessagesViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer123", password="superpass"
        )
        self.otherUser = User.objects.create_user(
            username="otherCustomer", password="superpass"
        )
        self.staffUser = User.objects.create_user(
            username="customerAgent123", password="superpass", is_staff=True
        )

        self.support_case = SupportCase.objects.create(from_user=self.user)

    def test_user_cannot_send_message_to_inexistent_support_case(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("messages_create", kwargs={"id": 999_999_999}),
            data={"content": "Something something 123"},
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_user_cannot_send_message_to_support_case_from_other_user(self):
        self.client.force_login(self.otherUser)

        response = self.client.post(
            reverse("messages_create", kwargs={"id": self.support_case.id}),
            data={"content": "Wow, this is really helpful!"},
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_user_can_send_message_to_their_support_case(self):
        self.client.force_login(self.user)

        message = "Hello, could you help me with my computer?"
        response = self.client.post(
            reverse("messages_create", kwargs={"id": self.support_case.id}),
            data={"content": message},
            follow=True,
        )
        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRegex(html_content, r"Support Case #[\d]+")
        self.assertIn("Your message was added to the support case.", html_content)
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        self.assertIn(message, html_content)

    def test_staff_user_can_send_message_to_any_support_case(self):
        self.client.force_login(self.staffUser)

        message = "Hello, I am here to help you."
        response = self.client.post(
            reverse("messages_create", kwargs={"id": self.support_case.id}),
            data={"content": message},
            follow=True,
        )
        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRegex(html_content, r"Support Case #[\d]+")
        self.assertIn("Your message was added to the support case.", html_content)
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        self.assertIn(message, html_content)

    def test_user_cannot_send_empty_message(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("messages_create", kwargs={"id": self.support_case.id}),
            data={"content": ""},
        )

        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn("Your message was added to the support case.", html_content)
