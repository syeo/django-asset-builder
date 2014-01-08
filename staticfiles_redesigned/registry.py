from django.utils.functional import SimpleLazyObject

from staticfiles_redesigned.conf import settings

class BaseRegistry(object):
    def __init__(self):
        from staticfiles_redesigned.factories.asset_factory import AssetFactory
        self.asset_factory = AssetFactory()
        from staticfiles_redesigned.repositories import AssetRepository
        self.asset_repository = AssetRepository()
        from staticfiles_redesigned.services.asset_manifest_service import AssetManifestService
        self.asset_manifest_service = AssetManifestService()
        from staticfiles_redesigned.repositories import AssetManifestRepository
        self.asset_manifest_repository = AssetManifestRepository()
        from staticfiles_redesigned.factories.asset_manifest_factory import AssetManifestFactory
        self.asset_manifest_factory = AssetManifestFactory()
        from staticfiles_redesigned.services.finder_service import FinderService
        self.finder_service = FinderService()
        from staticfiles_redesigned.repositories import AssetLineRepository
        self.asset_line_repository = AssetLineRepository()

class DebugRegistry(BaseRegistry):
    def __init__(self):
        from staticfiles_redesigned.services.asset_service import DebugAssetService
        self.asset_service = DebugAssetService()
        super(DebugRegistry, self).__init__()

class ReleaseRegistry(BaseRegistry):
    def __init__(self):
        from staticfiles_redesigned.services.asset_service import ReleaseAssetService
        self.asset_service = ReleaseAssetService()
        super(ReleaseRegistry, self).__init__()

if settings.SR_ENABLED:
    registry_class = ReleaseRegistry
else:
    registry_class = DebugRegistry

registry_instance = SimpleLazyObject(lambda: registry_class())
