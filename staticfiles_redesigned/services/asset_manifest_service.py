from __future__ import unicode_literals

import os

from staticfiles_redesigned.registry import registry_instance
from staticfiles_redesigned.models.assets import AssetLine
from staticfiles_redesigned.models.asset_manifests import JSAssetManifest, CSSAssetManifest

class AssetManifestService(object):
    def process_asset_manifest(self, asset_manifest):
        asset_manifest.clear()
        asset_manifest_context = AssetManifestContext.create_asset_manifest_context_with_asset_manifest(asset_manifest)
        AssetManifestProcessor.require_asset(asset_manifest_context, asset_manifest.root_asset)
        for asset in asset_manifest.get_assets():
            asset_manifest.add_asset_lines(registry_instance.asset_line_repository.get_content_lines_from_asset(asset))

class AssetManifestContext(object):
    @staticmethod
    def create_asset_manifest_context_with_asset_manifest(asset_manifest):
        if isinstance(asset_manifest, JSAssetManifest):
            return AssetManifestContext(asset_manifest, 'js')
        elif isinstance(asset_manifest, CSSAssetManifest):
            return AssetManifestContext(asset_manifest, 'css')
        else:
            raise Exception()

    def __init__(self, asset_manifest, ext):
        self.asset_manifest = asset_manifest
        self.visited_assets = set()
        self.ext = ext

    def mark_asset_visited(self, asset):
        self.visited_assets.add(asset)

    def is_asset_visited(self, asset):
        return asset in self.visited_assets

    def is_asset_related(self, asset):
        return asset.ext == self.ext

class AssetManifestProcessor(object):
    @staticmethod
    def get_new_asset_with_relative_path(asset, relative_path):
        new_logical_path = os.path.normpath(os.path.join(os.path.dirname(asset.logical_path), relative_path) + "." + asset.ext)
        return registry_instance.asset_repository.get_asset_with_logical_path(new_logical_path)

    @staticmethod
    def require_asset(asset_manifest_context, asset):
        if asset_manifest_context.is_asset_visited(asset):
            raise Exception()
        else:
            asset_manifest_context.mark_asset_visited(asset)

        self_required = False

        directive_lines = registry_instance.asset_line_repository.get_directive_lines_from_asset(asset)
        for directive_line in directive_lines:
            if directive_line.type == AssetLine.REQUIRE_SELF:
                asset_manifest_context.asset_manifest.add_asset(asset)
                self_required = True
            elif directive_line.type == AssetLine.REQUIRE:
                new_asset = AssetManifestProcessor.get_new_asset_with_relative_path(asset, directive_line.path)
                AssetManifestProcessor.require_asset(asset_manifest_context, new_asset)
            else:
                raise Exception()

        if not self_required:
            asset_manifest_context.asset_manifest.add_asset(asset)
