from helpdesk.models import Field, Node
from helpdesk.utils import HelpDeskTree

import uuid


def create_branch(branch):
    def copy_elem(obj, childs, *args, **kwargs):
        obj.original_id = obj.id
        obj.id = None
        obj.branch = branch
        obj.save()
        obj.childs.set(childs)

    HelpDeskTree().add_func(copy_elem).execute()


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

        childs = set(childs.values_list("original_id", flat=True))
        org_childs = set(obj.original.childs.all().values_list("id", flat=True))
        if childs ^ org_childs:
            return differences[key].append(obj.id)

        for field in obj.get_fields_names:
            if getattr(obj.original, field) != getattr(obj, field) and field != "parent":
                return differences[key].append(obj.id)

    tree.add_func(check_identical).execute()

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

            obj.childs.set([child.original for child in branch_obj.childs.all() if child.original])
            
            return 

        # Оригинальные дети - наше всё

        obj.original.childs.set([child.original for child in obj.childs.all() if child.original])

        # Перебираем поля чувствительные к версионности
        # И сравниваем с полями оригинального объекта

        for field in obj.get_fields_names:
            if getattr(obj.original, field) != getattr(obj, field) and field != "parent":
                setattr(obj.original, field, getattr(obj, field))

        version = uuid.uuid4()
        obj.version = version
        obj.save()
        obj.original.version = version
        obj.original.save()

    tree.add_func(merge).execute()

    pull.status = 2
    pull.save()
