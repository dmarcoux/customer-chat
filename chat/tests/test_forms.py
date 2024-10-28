from django.forms.models import model_to_dict
from django.test import TestCase

from chat.forms import MessageForm
from chat.models import Message, SupportCase, User


class MessageFormTestCase(TestCase):
    def setUp(self) -> None:
        self.messageContent = "This is a short message"
        self.form = MessageForm(data={"content": self.messageContent})
        self.form.is_valid()
        self.fromUser = User.objects.create_user(username="aCustomer1", password="something123")
        self.fromUser.save()
        self.supportCase = SupportCase.objects.create(from_user=self.fromUser)
        self.supportCase.save()

    def test_create_message(self) -> None:
        initial_messages_count = Message.objects.count()

        self.form.create_message(self.supportCase, self.fromUser)

        assert Message.objects.count() == initial_messages_count + 1
        assert model_to_dict(Message.objects.last(), exclude=["id"]) == {
            "content": self.messageContent,
            "from_user": self.fromUser.id,
            "support_case": self.supportCase.id,
        }
