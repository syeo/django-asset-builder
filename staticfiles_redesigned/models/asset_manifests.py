from __future__ import unicode_literals

from django.contrib.staticfiles.storage import staticfiles_storage

class AssetManifest(object):
    def __init__(self, asset):
        self.root_asset = asset
        self.assets = []
        self.content_lines = []

    def get_urls(self):
        for asset in self.assets:
            yield staticfiles_storage.url(asset.logical_path)

    def get_content_lines(self):
        for content_line in self.content_lines:
            yield content_line

    def get_assets(self):
        for asset in self.assets:
            yield asset

    def clear(self):
        self.assets = []
        self.content_lines = []

    def add_asset(self, asset):
        self.assets.append(asset)

    def add_content_line(self, content_line):
        self.content_lines.append(content_line)

    def add_asset_lines(self, asset_lines):
        for asset_line in asset_lines:
            self.add_content_line(asset_line.content)

class CSSAssetManifest(AssetManifest):
    pass

class JSAssetManifest(AssetManifest):
    pass
