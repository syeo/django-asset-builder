from __future__ import unicode_literals

from django.core.files.base import ContentFile
from django.utils.encoding import force_bytes
from django.contrib.staticfiles.storage import staticfiles_storage

from staticfiles_redesigned.models.assets import GenericAsset
from staticfiles_redesigned.registry import registry_instance

class AssetService(object):
    def get_compiled_content_file(self, asset):
        if isinstance(asset, GenericAsset):
            return registry_instance.finder_service.open_asset(asset)
        else:
            ret = ContentFile('')
            asset_manifest = registry_instance.asset_manifest_repository.get_asset_manifest_with_asset(asset)
            for content_line in asset_manifest.get_content_lines():
                ret.write(force_bytes(content_line))
                ret.write(force_bytes("\n"))
            return ret

class UnprocessedAssetService(AssetService):
    def get_urls(self, asset):
        asset_manifest = registry_instance.asset_manifest_repository.get_asset_manifest_with_asset(asset)
        return asset_manifest.get_urls()

class ProcessedAssetService(AssetService):
    def get_urls(self, asset):
        return [staticfiles_storage.url(asset.logical_path, True)]