from django import template

from wagtail.core.models import Page

from wagtail_deesign.design_center.models import Header

register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/

@register.inclusion_tag('deseign_center/include/header_text.html', takes_context=True)
def get_header_text(context):
    header_text = ""
    if Header.objects.first() is not None:
        header_text = Header.objects.first().body

    return {
        'header_text': header_text,
    }
