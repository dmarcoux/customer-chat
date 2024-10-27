from django.test import TestCase
from ..models import SupportCase


class SupportCaseTestCase(TestCase):
    def setUp(self):
        self.supportCase = SupportCase(id="123")

    def test___str__(self):
        self.assertEqual(str(self.supportCase), "Support Case #123")
