from django.conf import settings

DEBUG = getattr(settings, 'STATICFILES_REDESIGNED_DEBUG', settings.DEBUG)

MIMETYPES = {
    '.css': 'text/css',
    '.js': 'application/javascript'
}
MIMETYPES.update(**getattr(settings, 'MIMETYPES', {}))

MINIFY_TEXT_ASSETS = getattr(settings, 'MINIFY_TEXT_ASSETS', False)

# FINDER = getattr(settings, 'STATICFILES_REDESIGNED_FINDER', 'staticassets.finder.AssetFinder')

# PREPROCESSORS = getattr(settings, 'STATICFILES_REDESIGNED_PREPROCESSORS', (
#     ('application/javascript', 'staticassets.processors.DirectiveProcessor'),
#     ('text/css', 'staticassets.processors.DirectiveProcessor')
# ))

# POSTPROCESSORS = getattr(settings, 'STATICFILES_REDESIGNED_POSTPROCESSORS', tuple())

# COMPILERS = {
#     '.sass': 'staticassets.compilers.SassCompiler',
#     '.scss': 'staticassets.compilers.SassCompiler',
#     '.styl': 'staticassets.compilers.StylusCompiler',
#     '.less': 'staticassets.compilers.LessCompiler',
#     '.jst': 'staticassets.compilers.JstCompiler',
#     '.ejs': 'staticassets.compilers.EjsCompiler',
#     '.coffee': 'staticassets.compilers.CoffeeScriptCompiler'
# }
# COMPILERS.update(**getattr(settings, 'STATICFILES_REDESIGNED_COMPILERS', {}))

# AVAILABLE_EXTENSIONS = MIMETYPES.keys() + COMPILERS.keys()
