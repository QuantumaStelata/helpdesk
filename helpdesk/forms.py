from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from .models import Field, Node


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = "__all__"
        widgets = {
            "creator": forms.HiddenInput(),
            "branch": forms.HiddenInput(),
            "version": forms.HiddenInput(),
            "original": forms.HiddenInput(),
            "parent": forms.HiddenInput(),
            "is_start": forms.HiddenInput(),
            "deleted": forms.HiddenInput(),
        }
        labels = {
            "type": "Тип",
            "label": "Назва поля",
            "placeholder": "Заповнювач",
            "help_text": "Підказка",
            "min_length": "Мінімальна довжина",
            "max_length": "Максимальна довжина",
            "required": "Обов'язкове поле",
            "initial": "Початкові дані"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["label"].widget.attrs["rows"] = 2
        self.fields["help_text"].widget.attrs["rows"] = 2

        self.helper = FormHelper()
        self.helper.form_action = None
        self.helper.layout = Layout(
            "type", "label", "help_text",
            Row(
                Column("placeholder"),
                Column("initial")
            ),
            Row(
                Column("min_length"),
                Column("max_length")
            ),
            "required", "version", "parent", "branch", "creator"
        )


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = "__all__"
        widgets = {
            "creator": forms.HiddenInput(),
            "branch": forms.HiddenInput(),
            "version": forms.HiddenInput(),
            "original": forms.HiddenInput(),
            "parent": forms.HiddenInput(),
            "deleted": forms.HiddenInput(),
        }
        labels = {
            "text": "Текст",
            "value": "Значення",
            "is_active": "Об'єкт активован"
        }
