from __future__ import unicode_literals

import os

from django.contrib.staticfiles.storage import CachedFilesMixin, StaticFilesStorage, staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import get_storage_class
from django.utils.datastructures import SortedDict
from django.utils.functional import SimpleLazyObject

from staticfiles_redesigned.conf import settings

path_level = lambda name: len(name.split(os.sep))

class SRMixin(object):
    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name

class SRStaticfilesStorage(SRMixin, StaticFilesStorage):
    pass

class SRCachedStaticfilesStorage(SRMixin, CachedFilesMixin, StaticFilesStorage):
    pass

class SRCompressedCachedStaticfilesStorage(SRMixin, CachedFilesMixin, StaticFilesStorage):
    def get_compressed_name(self, name):
        name_root, ext = os.path.splitext(name)
        if ext.lower() == '.js' or ext.lower() == '.css':
            return "%s.min%s" % (name_root, ext)
        else:
            return name

    def url(self, name, force=False):
        if not settings.DEBUG or force:
            compressed_name = self.get_compressed_name(name)
            if self.exists(compressed_name):
                name = compressed_name
        return super(SRCompressedCachedStaticfilesStorage, self).url(name, force)

class SRCollectstaticStorageMixin(object):
    prefix = None

    def __init__(self, *args, **kwargs):
        location = settings.SR_COLLECTSTATIC_TEMPORARY_DIR
        if not location:
            raise Exception()
        super(SRCollectstaticStorageMixin, self).__init__(location, *args, **kwargs)

    def post_process(self, paths, dry_run = False, **options):
        paths = self.copy_files_to_original_staticfiles_storage(paths, dry_run)
        if hasattr(staticfiles_storage, 'post_process'):
            return staticfiles_storage.post_process(paths, dry_run, **options)
        else:
            return [(path, path, True) for path in paths]

    def copy_files_to_original_staticfiles_storage(self, paths, dry_run = False):
        if dry_run:
            return {}
        new_paths = SortedDict()
        for name in sorted(paths.keys(), key=path_level, reverse=True):
            if name not in new_paths:
                staticfiles_storage.save(name, self.open(name))
                new_paths[name] = (self, name)
        return new_paths

class SRCollectstaticStorage(SRMixin, SRCollectstaticStorageMixin, FileSystemStorage):
    pass

class SRCompressCollectstaticStorage(SRMixin, SRCollectstaticStorageMixin, FileSystemStorage):
    def execute_command(self, command):
        import subprocess
        pipe = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = pipe.communicate()
        if stderr.strip():
            raise Exception()

    def compress_js_file(self, source_name, target_name):
        command = '/usr/bin/env uglifyjs %s --mangle=sort --output=%s' % (self.path(source_name), self.path(target_name))
        self.execute_command(command)

    def compress_css_file(self, source_name, target_name):
        command = '/usr/bin/env cssmin %s > %s' % (self.path(source_name), self.path(target_name))
        self.execute_command(command)

    def compress_files(self, paths, dry_run):
        new_paths = SortedDict()
        for name in sorted(paths.keys(), key=path_level, reverse=True):
            new_paths[name] = paths[name]
            name_root, ext = os.path.splitext(name)
            if ext.lower() == '.js' or ext.lower() == '.css':
                target_name = "%s.min%s" % (name_root, ext)
                if ext == '.js':
                    self.compress_js_file(name, target_name)
                else:
                    self.compress_css_file(name, target_name)
                new_paths[target_name] = (self, target_name)
        return new_paths

    def post_process(self, paths, dry_run = False, **options):
        paths = self.compress_files(paths, dry_run)
        return super(SRCompressCollectstaticStorage, self).post_process(paths, dry_run, **options)

collectstatic_storage = SimpleLazyObject(lambda: get_storage_class(settings.SR_COLLECTSTATIC_STORAGE)())
