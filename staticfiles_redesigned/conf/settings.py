from django.conf import settings

SR_ENABLED = getattr(settings, "SR_ENABLED", not settings.DEBUG)

SR_COLLECTSTATIC_STORAGE = getattr(settings, 'SR_COLLECTSTATIC_STORAGE')
SR_COLLECTSTATIC_TEMPORARY_DIR = getattr(settings, 'SR_COLLECTSTATIC_TEMPORARY_DIR')
