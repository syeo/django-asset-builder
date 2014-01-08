import os

from staticfiles_redesigned.registry import registry_instance
from staticfiles_redesigned.models.assets import AssetLine

class AssetRepository(object):
    def get_asset_with_logical_path(self, logical_path):
        _, ext = os.path.splitext(logical_path)
        ext = ext.lstrip('.').lower()
        if ext == 'js':
            return registry_instance.asset_factory.create_js_asset_with_logical_path(logical_path)
        elif ext == 'css':
            return registry_instance.asset_factory.create_css_asset_with_logical_path(logical_path)
        else:
            return registry_instance.asset_factory.crete_generic_asset_with_logical_path(logical_path)

class AssetManifestRepository(object):
    def get_asset_manifest_with_asset(self, asset):
        return registry_instance.asset_manifest_factory.create_asset_manifest_with_asset(asset)

class AssetInterpreter(object):
    def __init__(self, single_line_comment_mark, has_mutiple_line_comment):
        self.single_line_comment_mark = single_line_comment_mark
        self.has_mutiple_line_comment = has_mutiple_line_comment

        if self.single_line_comment_mark:
            self.single_line_comment_directive_mark = self.single_line_comment_mark + "="
        else:
            self.single_line_comment_directive_mark = None

        if self.has_mutiple_line_comment:
            self.multiple_line_comment_open_mark = '/*'
            self.multiple_line_comment_close_mark = '*/'
            self.multiple_line_comment_continue_mark = '*'
            self.multiple_line_comment_directive_mark = self.multiple_line_comment_continue_mark + "="
        else:
            self.multiple_line_comment_open_mark = None
            self.multiple_line_comment_close_mark = None
            self.multiple_line_comment_continue_mark = None
            self.multiple_line_comment_directive_mark = None

        self.multi_line_comment_opened = False
        self.manifest_ended = False

    def is_line_multi_line_directive(self, line):
        stripped_line = line.strip()
        return self.multiple_line_comment_directive_mark and stripped_line.startswith(self.multiple_line_comment_directive_mark)

    def is_line_closing_multi_line_comment(self, line):
        stripped_line = line.strip()
        return self.multiple_line_comment_close_mark and stripped_line.endswith(self.multiple_line_comment_close_mark)

    def is_line_opening_multi_line_comment(self, line):
        stripped_line = line.strip()
        return self.multiple_line_comment_open_mark and stripped_line.startswith(self.multiple_line_comment_open_mark)

    def is_line_single_line_directive(self, line):
        stripped_line = line.strip()
        return self.single_line_comment_directive_mark and stripped_line.startswith(self.single_line_comment_directive_mark)

    def interpret_directive_line(self, line):
        splitted_line = line.split()
        if splitted_line[1] == 'require':
            return AssetLine.create_require(splitted_line[2])
        elif splitted_line[1] == 'require_self':
            return AssetLine.create_require_self()
        else:
            # TODO(stan): need to implement 'require_tree', 'require_dir'
            raise Exception()

    def interpret_line(self, line):
        line = line.rstrip()
        if self.manifest_ended:
            return AssetLine.create_content_line(line)
        else:
            if self.multi_line_comment_opened:
                if self.is_line_multi_line_directive(line):
                    return self.interpret_directive_line(line)
                else:
                    if self.is_line_closing_multi_line_comment(line):
                        self.multi_line_comment_opened = False
                    return AssetLine.create_content_line(line)
            else:
                if self.is_line_opening_multi_line_comment(line):
                    self.multi_line_comment_opened = True
                    return AssetLine.create_content_line(line)
                elif self.is_line_single_line_directive(line):
                    return self.interpret_directive_line(line)
                else:
                    self.manifest_ended = True
                    return AssetLine.create_content_line(line)

class AssetLineRepository(object):
    def get_lines_from_asset(self, asset):
        lines = registry_instance.finder_service.get_lines_from_asset(asset)
        asset_manifest_interpreter = AssetInterpreter(*asset.comment_syntax)
        for line in lines:
            yield asset_manifest_interpreter.interpret_line(line)

    def get_content_lines_from_asset(self, asset):
        for asset_source_line in self.get_lines_from_asset(asset):
            if not asset_source_line.is_directive:
                yield asset_source_line

    def get_directive_lines_from_asset(self, asset):
        for asset_source_line in self.get_lines_from_asset(asset):
            if asset_source_line.is_directive:
                yield asset_source_line
