from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import render_to_string

from staticfiles_redesigned.registry import registry_instance

register = template.Library()

class SRURLNode(template.Node):
    def __init__(self, logical_path_var):
        self.logical_path_var = logical_path_var

    def render(self, context):
        logical_path = template.Variable(self.logical_path_var).resolve(context)
        return staticfiles_storage.url(logical_path)

class SRAssetNode(object):
    def __init__(self, logical_path_var):
        self.logical_path_var = logical_path_var

    def render(self, context):
        return self.render_asset_to_string(self.get_asset(context))

    def get_asset(self, context):
        raise NotImplementedError()

    def render_template_to_string(self, template_path, context):
        return render_to_string(template_path, context)

    def render_asset_to_string(self, asset):
        urls = registry_instance.asset_service.get_urls(asset)
        return self.render_urls_to_string(urls)

    def render_urls_to_string(self, urls):
        return "\n".join([self.render_url_to_string(url) for url in urls])

    def render_url_to_string(self, url):
        raise NotImplementedError()

class SRCSSNode(SRAssetNode, template.Node):
    def get_asset(self, context):
        logical_path = ".".join([template.Variable(self.logical_path_var).resolve(context), "css"])
        return registry_instance.asset_repository.get_asset_with_logical_path(logical_path)

    def render_url_to_string(self, url):
        return self.render_template_to_string("staticfiles_redesigned/url_css.html", {'url': url})

class SRJSNode(SRAssetNode, template.Node):
    def get_asset(self, context):
        logical_path = ".".join([template.Variable(self.logical_path_var).resolve(context), "js"])
        return registry_instance.asset_repository.get_asset_with_logical_path(logical_path)

    def render_url_to_string(self, url):
        return self.render_template_to_string("staticfiles_redesigned/url_js.html", {'url': url})

@register.tag
def sr_url(parser, token):
    try:
        tag_name, path_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return SRURLNode(path_var)

@register.tag
def sr_css(parser, token):
    try:
        tag_name, logical_path_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r requires exactly one argument.' % token.split_contents()[0])
    return SRCSSNode(logical_path_var)

@register.tag
def sr_js(parser, token):
    try:
        tag_name, logical_path_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r requires exactly one argument.' % token.split_contents()[0])
    return SRJSNode(logical_path_var)
