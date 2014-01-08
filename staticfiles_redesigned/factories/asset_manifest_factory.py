from __future__ import unicode_literals

from staticfiles_redesigned.models.assets import CSSAsset, JSAsset
from staticfiles_redesigned.models.asset_manifests import CSSAssetManifest, JSAssetManifest
from staticfiles_redesigned.registry import registry_instance

class AssetManifestFactory(object):
    def create_asset_manifest_with_asset(self, asset):
        if isinstance(asset, JSAsset):
            asset_manifest = JSAssetManifest(asset)
        elif isinstance(asset, CSSAsset):
            asset_manifest = CSSAssetManifest(asset)
        else:
            raise Exception()
        registry_instance.asset_manifest_service.process_asset_manifest(asset_manifest)
        return asset_manifest
