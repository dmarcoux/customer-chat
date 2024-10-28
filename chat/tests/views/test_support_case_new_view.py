from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from chat.models import User


class SupportCaseNewViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="customer123", password="superpassword")
        self.staffUser = User.objects.create_user(username="customerAgent123", password="superpassword", is_staff=True)

    def test_unauthorized_for_user_is_staff(self) -> None:
        self.client.force_login(self.staffUser)

        response = self.client.get(reverse("support_cases_new"))

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_renders_for_user(self) -> None:
        self.client.force_login(self.user)

        response = self.client.get(reverse("support_cases_new"))
        html_content = response.content.decode()

        assert response.status_code == HTTPStatus.OK
        # This is a bit naive, but checking more would involve parsing the HTML (like with BeautifulSoup)
        assert "Open a Support Case" in html_content
