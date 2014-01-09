from staticfiles_redesigned.registry import registry_instance

class AssetManifestRepository(object):
    def get_asset_manifest_with_asset(self, asset):
        return registry_instance.asset_manifest_factory.create_asset_manifest_with_asset(asset)

class CachedAssetManifestRepository(AssetManifestRepository):
    def __init__(self):
        self.cached_asset_manifests = {}

    def get_asset_manifest_with_asset(self, asset):
        if not self.cached_asset_manifests.has_key(asset):
            self.cached_asset_manifests[asset] = super(CachedAssetManifestRepository, self).get_asset_manifest_with_asset(asset)
        return self.cached_asset_manifests[asset]
