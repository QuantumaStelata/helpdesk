from django.db import transaction

from .models import Field, Node


class HelpDeskTree:
    def __init__(self, queryset=None):
        self.queryset = queryset if queryset else Field.objects.filter(branch__isnull=True, is_start=True)

        self.prefuncs = []
        self.postfuncs = []

    def add_pre_deepening(self, func):
        if not callable(func):
            raise TypeError(f"{func} is not callable")
        
        self.prefuncs.append(func)
        return self
    
    def add_post_deepening(self, func):
        if not callable(func):
            raise TypeError(f"{func} is not callable")
        
        self.postfuncs.append(func)
        return self

    def recursion(self, queryset):
        for obj in queryset:

            for func in self.prefuncs:
                if result := func(obj):
                    self.recursion_return.append(result)

            if isinstance(obj, Field):
                childs = self.recursion(obj.child_nodes.all().select_related("original"))
            elif isinstance(obj, Node):
                childs = self.recursion(obj.child_fields.all().select_related("original"))
            else:
                raise TypeError(f"{obj} is not Field or Node")

            for func in self.postfuncs:
                if result := func(obj, childs):
                    self.recursion_return.append(result)
        
        return queryset
    
    @transaction.atomic
    def execute(self):
        self.recursion_return = []
        self.recursion(self.queryset)
        return self.recursion_return
