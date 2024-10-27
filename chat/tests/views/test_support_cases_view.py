from django.test import TestCase
from django.urls import reverse
from django.forms.models import model_to_dict
from ...models import User, SupportCase, Message
from http import HTTPStatus


class SupportCasesViewTestCase(TestCase):
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

        self.supportCaseUser1 = SupportCase.objects.create(from_user=self.user)
        self.supportCaseUser2 = SupportCase.objects.create(from_user=self.user)
        self.supportCaseOtherUser = SupportCase.objects.create(from_user=self.otherUser)

    def test_get_show_all_support_cases_for_staff(self):
        self.client.force_login(self.staffUser)

        response = self.client.get(reverse("support_cases"))
        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn("Open a support case", html_content)

        supportCases = [
            self.supportCaseUser1,
            self.supportCaseUser2,
            self.supportCaseOtherUser,
        ]
        for supportCase in supportCases:
            self.assertInHTML(
                f'<a href="{reverse("support_cases_show", kwargs={"id": supportCase.id})}">Support Case #{supportCase.id}</a>',
                html_content,
            )

    def test_get_show_support_cases_only_for_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("support_cases"))
        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Open a support case", html_content)

        supportCases = [self.supportCaseUser1, self.supportCaseUser2]
        for supportCase in supportCases:
            self.assertInHTML(
                f'<a href="{reverse("support_cases_show", kwargs={"id": supportCase.id})}">Support Case #{supportCase.id}</a>',
                html_content,
            )

        self.assertNotInHTML(
            f'<a href="{reverse("support_cases_show", kwargs={"id": self.supportCaseOtherUser.id})}">Support Case #{self.supportCaseOtherUser.id}</a>',
            html_content,
        )

    def test_post_user_staff_unauthorized_to_open_support_case(self):
        self.client.force_login(self.staffUser)

        response = self.client.post(
            reverse("support_cases"), data={"content": "Hello!"}
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_user_can_open_support_case(self):
        self.client.force_login(self.user)

        initialSupportCasesCount = SupportCase.objects.count()

        message = "Hello! I need your help with my bike."
        response = self.client.post(
            reverse("support_cases"),
            data={"content": message},
        )

        supportCase = SupportCase.objects.last()

        self.assertRedirects(
            response, reverse("support_cases_show", kwargs={"id": supportCase.id})
        )
        self.assertEqual(SupportCase.objects.count(), initialSupportCasesCount + 1)
        self.assertEqual(
            model_to_dict(supportCase, exclude=["id"]),
            {
                "from_user": self.user.id,
            },
        )
        self.assertEqual(
            model_to_dict(Message.objects.last(), exclude=["id"]),
            {
                "content": message,
                "from_user": self.user.id,
                "support_case": supportCase.id,
            },
        )

    def test_post_user_cannot_open_support_case_when_message_is_empty(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("support_cases"), data={"content": ""})

        html_content = response.content.decode()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Your support case could not be opened. Try again.", html_content)
