from django.conf import settings
from django.db import transaction, models

from helpdesk.models import Field, Node
from .models import Branch

from functools import lru_cache
import time
import uuid


def get_ttl(seconds=600):
    """For lru_cache time to live"""
    return round(time.time() / seconds)


@transaction.atomic
def create_branch(branch):
    start_field = Field.objects.filter(is_start=True, branch__isnull=True)

    def recursion(queryset):
        objs = []

        for obj in queryset:
            if isinstance(obj, Field):
                nodes = recursion(obj.child_nodes.all())

                obj.original_id = obj.id
                obj.id = None
                obj.branch = branch
                obj.save()
                obj.child_nodes.set(nodes)

            elif isinstance(obj, Node):
                fields = recursion(obj.child_fields.all())

                obj.original_id = obj.id
                obj.id = None
                obj.branch = branch
                obj.save()
                obj.child_fields.set(fields)
            
            objs.append(obj)

        return objs

    return recursion(start_field)


# @lru_cache
def pull_detail(pull, ttl=None):
    start_field = Field.objects.filter(is_start=True, branch_id=pull.branch_id)

    def recursion(queryset):
        differences = {
            "fields": [],
            "nodes": [],
            "fields_conflict": [],
            "nodes_conflict": []
        }

        for obj in queryset:
            if isinstance(obj, Field):
                if obj.original and obj.version != obj.original.version:
                    pull.status = 4
                    differences["fields_conflict"].append(obj.id)

                child_diffs = recursion(obj.child_nodes.all())

                if obj.original and not obj.deleted:
                    fields = ["type", "label", "placeholder", "help_text", "min_length", "max_length", "required", "initial"]

                    for field in fields:
                        if getattr(obj.original, field) != getattr(obj, field):
                            differences["fields"].append(obj.id)
                            break        
                else:
                    differences["fields"].append(obj.id)

            elif isinstance(obj, Node):
                if obj.original and obj.version != obj.original.version:
                    pull.status = 4
                    differences["nodes_conflict"].append(obj.id)

                child_diffs = recursion(obj.child_fields.all())

                if obj.original and not obj.deleted:
                    fields = ["text", "value", "is_active"]

                    for field in fields:
                        if getattr(obj.original, field) != getattr(obj, field):
                            differences["fields"].append(obj.id)
                            break        
                else:
                    differences["fields"].append(obj.id)
            
            differences["fields"] += child_diffs["fields"]
            differences["nodes"] += child_diffs["nodes"]

        return differences


    pull.status = 1 if pull.status == 4 else pull.status
    detail = recursion(start_field)
    pull.save()

    return detail


@transaction.atomic
def pull_merge(pull):        
    def recursion(queryset):
        for obj in queryset:
            if isinstance(obj, Field):
                recursion(obj.child_nodes.all())

            elif isinstance(obj, Node): 
                recursion(obj.child_fields.all())

            if not obj.original:
                obj.branch = None
                continue

            for field in obj.get_fields_names:
                if hasattr(getattr(obj.original, field), "through"):
                    pass
                    # setattr(obj.original, field, getattr(obj, field))
                    # m2m_changed.connect(cls.m2m_changed, getattr(getattr(cls, field), "through"))
                elif getattr(obj.original, field) != getattr(obj, field):   
                    setattr(obj.original, field, getattr(obj, field))

            version = uuid.uuid4()
            obj.version = version
            obj.save()

            if obj.original:
                obj.original.version = version
                obj.original.save()
        
        return True
    
    start_field = Field.objects.filter(is_start=True, branch=pull.branch)

    if merged := recursion(start_field):
        pull.status = 2
        pull.save()
    return merged
