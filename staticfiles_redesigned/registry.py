from django.utils.functional import SimpleLazyObject

from staticfiles_redesigned.conf import settings

class Registry(object):
    def __init__(self):
        from staticfiles_redesigned.factories.asset_factory import AssetFactory
        self.asset_factory = AssetFactory()
        from staticfiles_redesigned.repositories.asset_repository import AssetRepository
        self.asset_repository = AssetRepository()
        from staticfiles_redesigned.services.asset_manifest_service import AssetManifestService
        self.asset_manifest_service = AssetManifestService()
        from staticfiles_redesigned.repositories.asset_manifest_repository import AssetManifestRepository
        self.asset_manifest_repository = AssetManifestRepository()
        from staticfiles_redesigned.factories.asset_manifest_factory import AssetManifestFactory
        self.asset_manifest_factory = AssetManifestFactory()
        from staticfiles_redesigned.services.finder_service import FinderService
        self.finder_service = FinderService()
        from staticfiles_redesigned.repositories.asset_line_repository import CachedAssetLineRepository
        self.asset_line_repository = CachedAssetLineRepository()

        if settings.SR_ENABLED:
            from staticfiles_redesigned.services.asset_service import ProcessedAssetService
            self.asset_service = ProcessedAssetService()
            from staticfiles_redesigned.repositories.asset_manifest_repository import CachedAssetManifestRepository
            self.asset_manifest_repository = CachedAssetManifestRepository()
        else:
            from staticfiles_redesigned.services.asset_service import UnprocessedAssetService
            self.asset_service = UnprocessedAssetService()
            from staticfiles_redesigned.repositories.asset_manifest_repository import AssetManifestRepository
            self.asset_manifest_repository = AssetManifestRepository()

registry_instance = SimpleLazyObject(lambda: Registry())
