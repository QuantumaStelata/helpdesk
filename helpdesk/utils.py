from django.db import transaction

from .models import Field


class HelpDeskTree:
    def __init__(self, queryset=None):
        self.queryset = queryset if queryset else Field.objects.filter(branch__isnull=True, is_start=True)

        self.funcs = []

    def add_func(self, func):
        if not callable(func):
            raise TypeError(f"{func} is not callable")
        
        self.funcs.append(func)
        return self

    def recursion(self, queryset):
        for obj in queryset:

            childs = self.recursion(obj.childs.all())

            for func in self.funcs:
                if result := func(obj, childs):
                    self.recursion_return.append(result)

        return queryset
    
    @transaction.atomic
    def execute(self):
        self.recursion_return = []
        self.recursion(self.queryset)
        return self.recursion_return
