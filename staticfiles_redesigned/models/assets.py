from __future__ import unicode_literals

import os

class Asset(object):
    def __init__(self, logical_path):
        self.logical_path = logical_path
        # self.absolute_path = absolute_path
        _, ext = os.path.splitext(logical_path)
        self.ext = ext.lstrip('.').lower()
        self.dir = os.path.dirname(logical_path)

    def __hash__(self):
        return hash(self.logical_path)

    def __eq__(self, obj):
        return type(self) == type(obj) and self.logical_path == obj.logical_path

    def __cmp__(self, obj):
        if self.logical_path > obj.logical_path:
            return 1
        elif self.logical_path < obj.logical_path:
            return -1
        else:
            return 0

class CSSAsset(Asset):
    comment_syntax = (None, True)

class JSAsset(Asset):
    comment_syntax = ('//', True)

class GenericAsset(Asset):
    pass

class AssetLine(object):
    CONTENT = 1
    REQUIRE_SELF = 2
    REQUIRE = 3
    DIRECTIVE = [2, 3]

    def __init__(self, type):
        self.type = type

    @classmethod
    def create_content_line(cls, content):
        ret = cls(AssetLine.CONTENT)
        ret.content = content
        return ret

    @classmethod
    def create_require_self(cls):
        return cls(AssetLine.REQUIRE_SELF)

    @classmethod
    def create_require(cls, path):
        ret = cls(AssetLine.REQUIRE)
        ret.path = path
        return ret

    @property
    def is_directive(self):
        return self.type in AssetLine.DIRECTIVE

