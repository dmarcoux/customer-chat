from django.test import TestCase
from django.urls import reverse
from ...models import User, SupportCase, Message
from http import HTTPStatus


class SupportCaseShowViewTests(TestCase):
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
        self.message = Message.objects.create(
            support_case=self.support_case,
            from_user=self.user,
            content="Hello, I need help with my computer.",
        )

    def test_user_cannot_access_support_case_of_another_user(self):
        self.client.force_login(self.otherUser)

        response = self.client.get(
            reverse("support_cases_show", kwargs={"id": self.support_case.id})
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_user_can_access_their_support_case(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("support_cases_show", kwargs={"id": self.support_case.id})
        )

        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRegex(html_content, r"Support Case #[\d]+")
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        self.assertIn(self.message.content, html_content)

    def test_staff_user_can_access_support_case(self):
        self.client.force_login(self.staffUser)

        response = self.client.get(
            reverse("support_cases_show", kwargs={"id": self.support_case.id})
        )

        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRegex(html_content, r"Support Case #[\d]+")
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        self.assertIn(self.message.content, html_content)

    def test_404_when_support_case_does_not_exist(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("support_cases_show", kwargs={"id": 999_999_999})
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
