from django.test import TestCase

from chat.models import SupportCase


class SupportCaseTestCase(TestCase):
    def setUp(self) -> None:
        self.supportCase = SupportCase(id="123")

    def test___str__(self) -> None:
        assert str(self.supportCase) == "Support Case #123"
