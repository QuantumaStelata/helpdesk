from django.contrib import admin

from . import models


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("label", "type", "branch", "creator", "dt_create", "dt_update")


@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
    pass
