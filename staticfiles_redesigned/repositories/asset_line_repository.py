from staticfiles_redesigned.conf import settings
from staticfiles_redesigned.registry import registry_instance
from staticfiles_redesigned.models.assets import AssetLine

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

    def get_stripped_unicode_line(self, line):
        try:
            return line.strip().decode(settings.FILE_CHARSET)
        except:
            return False

    def is_line_multi_line_directive(self, line):
        stripped_line = self.get_stripped_unicode_line(line)
        return stripped_line and self.multiple_line_comment_directive_mark and stripped_line.startswith(self.multiple_line_comment_directive_mark)

    def is_line_closing_multi_line_comment(self, line):
        stripped_line = self.get_stripped_unicode_line(line)
        return stripped_line and self.multiple_line_comment_close_mark and stripped_line.endswith(self.multiple_line_comment_close_mark)

    def is_line_opening_multi_line_comment(self, line):
        stripped_line = self.get_stripped_unicode_line(line)
        return stripped_line and self.multiple_line_comment_open_mark and stripped_line.startswith(self.multiple_line_comment_open_mark)

    def is_line_single_line_directive(self, line):
        stripped_line = self.get_stripped_unicode_line(line)
        return stripped_line and self.single_line_comment_directive_mark and stripped_line.startswith(self.single_line_comment_directive_mark)

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

class CachedAssetLineRepository(AssetLineRepository):
    def __init__(self):
        self.cached_lines = {}

    def get_lines_from_asset(self, asset):
        if not self.cached_lines.has_key(asset):
            self.cached_lines[asset] = super(CachedAssetLineRepository, self).get_lines_from_asset(asset)
        return self.cached_lines[asset]
