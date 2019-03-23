from django.forms import ModelForm
from personal.models import Invite


class InviteForm(ModelForm):
    def __init__(self, **kwargs):
        self.course_id = kwargs.pop('course_id')
        self.sender_username = kwargs.pop('sender_username')
        super(InviteForm, self).__init__(**kwargs)

    def save(self, commit=True):
        obj = super(InviteForm, self).save(commit=False)
        obj.course_id = self.course_id
        obj.sender_username = self.sender_username
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Invite
        fields = '__all__'
        exclude = ['course_id', 'sender_username', ]
