from django.contrib import admin

from . import models


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "creator", "dt_create", "dt_update")

admin.site.register(models.PullRequest)
