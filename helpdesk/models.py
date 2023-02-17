from django.db import models

from vcs.models import VersionAbstract, DateEventAbstract, CreatorAbstract


class Field(VersionAbstract, DateEventAbstract, CreatorAbstract):
    TYPES = {
        "select": "Select",
        "radio": "Radio",
        "checkbox": "Checkbox",
        "text": "Text",
        "number": "Number",
        "date": "Date",
        "time": "Time",
        "datetime": "Datetime",
        "image": "Image",
        "file": "File",
    }

    type = models.CharField(max_length=10, choices=TYPES.items())
    label = models.TextField()
    placeholder = models.CharField(max_length=64, blank=True, default="Обери із списку")
    help_text = models.TextField(blank=True)
    min_length = models.IntegerField(blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    required = models.BooleanField(default=False)
    initial = models.CharField(max_length=64, blank=True)
    parent = models.ForeignKey("helpdesk.Node", on_delete=models.CASCADE, blank=True, null=True, related_name="childs")
    is_start = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class Node(VersionAbstract, DateEventAbstract, CreatorAbstract):
    text = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    parent = models.ForeignKey("helpdesk.Field", on_delete=models.CASCADE, blank=True, null=True, related_name="childs")
    deleted = models.BooleanField(default=False)
