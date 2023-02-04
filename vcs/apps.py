from django.apps import AppConfig
from django.db.models.signals import pre_save, m2m_changed


class VcsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vcs'

    def ready(self):
        super().ready()

        from .models import VersionAbstract

        for cls in VersionAbstract.__subclasses__():
            pre_save.connect(cls.pre_save, cls)

            for field in cls.get_fields_names:
                if hasattr(getattr(cls, field), "through"):
                    m2m_changed.connect(cls.m2m_changed, getattr(getattr(cls, field), "through"))
