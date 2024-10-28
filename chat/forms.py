from django import forms

from chat.models import Message, SupportCase, User


class MessageForm(forms.Form):
    content = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"placeholder": "Write a message...", "cols": False, "rows": "4"}),
    )

    def create_message(self, support_case: SupportCase, from_user: User) -> None:
        new_message = Message(
            support_case=support_case,
            from_user=from_user,
            content=self.cleaned_data["content"],
        )
        new_message.save()
