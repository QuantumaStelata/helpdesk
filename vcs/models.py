from django.db import models
from django.contrib.auth import get_user_model

import uuid


class DateEventAbstract(models.Model):
    dt_create = models.DateTimeField(auto_now_add=True, editable=False)
    dt_update = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class CreatorAbstract(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="%(class)ss")

    class Meta:
        abstract = True


class VersionAbstract(models.Model):
    branch = models.ForeignKey("vcs.Branch", on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)ss")
    version = models.UUIDField(default=uuid.uuid4)
    original = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True

    @classmethod
    def pre_save(cls, instance, *args, **kwargs):
        if instance.branch:
            return

        if pre_instance := cls.objects.filter(id=instance.id).first():
            if pre_instance.version != instance.version:
                return

            for field in instance.get_fields_names:
                if getattr(pre_instance, field) != getattr(instance, field):
                    instance.version = uuid.uuid4()
                    return
            
    @classmethod
    def m2m_changed(cls, instance, action, *args, **kwargs):
        if not instance.branch and action.startswith("post_"):
            instance.version = uuid.uuid4()
            instance.save()
    
    @classmethod
    @property
    def get_fields_names(cls):
        all_fields = set(field.name for field in cls._meta.fields + cls._meta.many_to_many if field.name != "id")
        parent_fields = set(field.name for field in VersionAbstract._meta.fields + VersionAbstract._meta.many_to_many if field.name != "id")
        return list(all_fields ^ parent_fields)


class Branch(DateEventAbstract, CreatorAbstract):
    name = models.CharField(max_length=128, unique=True)
    contributors = models.ManyToManyField(get_user_model(), blank=True, related_name="contribute_branchs")

    def __str__(self):
        return self.name


class PullRequest(DateEventAbstract, CreatorAbstract):
    STATUSES = {
        1: "Open",
        2: "Merged",
        3: "Closed",
        4: "Conflict",
        5: "Returned"
    }

    branch = models.ForeignKey("vcs.Branch", on_delete=models.CASCADE, related_name="pulls")
    status = models.IntegerField(choices=STATUSES.items(), default=1)
    completive = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="completive_pulls")