from helpdesk.models import Field, Node
from helpdesk.utils import HelpDeskTree

import uuid
from itertools import zip_longest


def create_branch(branch):
    tree = HelpDeskTree()

    def copy_elem(obj, childs, *args, **kwargs):
        obj.original_id = obj.id
        obj.id = None
        obj.branch = branch
        obj.save()

        if isinstance(obj, Field) and childs:
            obj.child_nodes.set(childs)
        elif isinstance(obj, Node) and childs:
            obj.child_fields.set(childs)

    tree.add_post_deepening(copy_elem).execute()


def pull_detail(pull):
    tree = HelpDeskTree(Field.objects.filter(is_start=True, branch_id=pull.branch_id).select_related("original"))
    
    differences = {
        "fields": [], "nodes": [],
        "conflicts": { "fields": [], "nodes": [] }
    }

    def check_identical(obj, childs, *args, **kwagrs):
        if isinstance(obj, Field):
            key = "fields"
        elif isinstance(obj, Node):
            key = "nodes"
        else:
            raise TypeError(f"{obj} is not Field or Node")

        if not obj.original:
            return differences[key].append(obj.id)
        
        if obj.original.version != obj.version:
            differences["conflicts"][key].append(obj.id)
        
        for field in obj.get_fields_names:
            if hasattr(getattr(obj.original, field), "through"):
                childs = childs.order_by("-original__id")
                org_childs = getattr(obj.original, field).all().order_by("-id").select_related("original")

                for child, org_child in zip_longest(childs, org_childs):
                    if not child or not org_child or not child.original or child.original_id != org_child.id:
                        return differences[key].append(obj.id)

            elif getattr(obj.original, field) != getattr(obj, field):
                return differences[key].append(obj.id)

    tree.add_post_deepening(check_identical).execute()

    return differences


def pull_merge(pull):
    tree = HelpDeskTree(Field.objects.filter(is_start=True, branch_id=pull.branch_id))

    def merge(obj, childs, *args, **kwargs):
        if not obj.original:
            obj.branch = None

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

        return obj, obj.original

    tree.add_post_deepening(merge).execute()

    pull.status = 2
    pull.save()
