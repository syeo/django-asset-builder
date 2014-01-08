from __future__ import unicode_literals

from staticfiles_redesigned.registry import registry_instance

from staticfiles_redesigned.models.assets import JSAsset, CSSAsset, GenericAsset

class AssetFactory(object):
    def create_css_asset_with_logical_path(self, logical_path):
        if registry_instance.finder_service.check_existance(logical_path):
            return CSSAsset(logical_path)
        else:
            raise Exception()

    def create_js_asset_with_logical_path(self, logical_path):
        if registry_instance.finder_service.check_existance(logical_path):
            return JSAsset(logical_path)
        else:
            raise Exception()

    def crete_generic_asset_with_logical_path(self, logical_path):
        if registry_instance.finder_service.check_existance(logical_path):
            return GenericAsset(logical_path)
        else:
            raise Exception()
