from helpdesk.models import Field, Node
from helpdesk.utils import HelpDeskTree

import uuid


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
                childs = set(childs.values_list("original_id", flat=True))
                org_childs = set(getattr(obj.original, field).all().values_list("id", flat=True))

                if childs ^ org_childs:
                    return differences[key].append(obj.id)

            elif getattr(obj.original, field) != getattr(obj, field):
                return differences[key].append(obj.id)

    tree.add_post_deepening(check_identical).execute()

    return differences


def pull_merge(pull):
    tree = HelpDeskTree(Field.objects.filter(is_start=True, branch_id=pull.branch_id))

    def merge(obj, childs, *args, **kwargs):
        if not obj.original:
            # Если у объекта в ветке нет оригинала, создаем его
            # Подвязываем объект в ветке к оригиналу и связываем с оригинальными дочерними объектами
            # После выходим из функции, т.к. нам не надо проверять соответствие полей

            branch_obj_id = obj.id

            obj.id = obj.branch = None
            obj.save()
            
            branch_obj = obj.__class__.objects.get(id=branch_obj_id)
            branch_obj.original_id = obj.id
            branch_obj.save()

            obj.child_fields.set([child.original for child in childs])
            
            return 

        # Перебираем поля чувствительные к версионности
        # И сравниваем с полями оригинального объекта

        for field in obj.get_fields_names:
            if hasattr(getattr(obj.original, field), "through"):
                getattr(obj.original, field).set(
                    [child.original for child in getattr(obj, field).all()]
                )
            elif getattr(obj.original, field) != getattr(obj, field):   
                setattr(obj.original, field, getattr(obj, field))

        version = uuid.uuid4()
        obj.version = version
        obj.save()
        obj.original.version = version
        obj.original.save()

    tree.add_post_deepening(merge).execute()

    pull.status = 2
    pull.save()
