import os

from staticfiles_redesigned.registry import registry_instance

class AssetRepository(object):
    def get_asset_with_logical_path(self, logical_path):
        _, ext = os.path.splitext(logical_path)
        if ext.lower() == '.js':
            return registry_instance.asset_factory.create_js_asset_with_logical_path(logical_path)
        elif ext.lower() == '.css':
            return registry_instance.asset_factory.create_css_asset_with_logical_path(logical_path)
        else:
            return registry_instance.asset_factory.crete_generic_asset_with_logical_path(logical_path)

