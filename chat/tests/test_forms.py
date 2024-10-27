from django.test import TestCase
from django.forms.models import model_to_dict
from ..forms import MessageForm
from ..models import User, SupportCase, Message


class MessageFormTestCase(TestCase):
    def setUp(self):
        self.messageContent = "This is a short message"
        self.form = MessageForm(data={"content": self.messageContent})
        self.form.is_valid()
        self.fromUser = User.objects.create_user(
            username="aCustomer1", password="something123"
        )
        self.fromUser.save()
        self.supportCase = SupportCase.objects.create(from_user=self.fromUser)
        self.supportCase.save()

    def test_create_message(self):
        initialMessagesCount = Message.objects.count()

        self.form.create_message(self.supportCase, self.fromUser)

        self.assertEqual(Message.objects.count(), initialMessagesCount + 1)
        self.assertEqual(
            model_to_dict(Message.objects.last(), exclude=["id"]),
            {
                "content": self.messageContent,
                "from_user": self.fromUser.id,
                "support_case": self.supportCase.id,
            },
        )
