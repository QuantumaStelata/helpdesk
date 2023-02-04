from django.db import models

from vcs.models import VersionAbstract, DateEventAbstract, CreatorAbstract


class Field(VersionAbstract, DateEventAbstract, CreatorAbstract):
    TYPES = {
        "select": "select",
        "radio": "radio",
        "checkbox": "checkbox",
        "text": "text",
        "number": "number",
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "image": "image",
        "file": "file",
    }

    type = models.CharField(max_length=10, choices=TYPES.items())
    label = models.CharField(max_length=128, blank=True)
    placeholder = models.CharField(max_length=128, blank=True)
    help_text = models.CharField(max_length=128, blank=True)
    min_length = models.IntegerField(blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    required = models.BooleanField(default=False)
    initial = models.CharField(max_length=128, blank=True)
    child_nodes = models.ManyToManyField("helpdesk.Node", blank=True, related_name="parent_fields")
    is_start = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class Node(VersionAbstract, DateEventAbstract, CreatorAbstract):
    text = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    child_fields = models.ManyToManyField("helpdesk.Field", blank=True, related_name="parent_nodes")
    deleted = models.BooleanField(default=False)
