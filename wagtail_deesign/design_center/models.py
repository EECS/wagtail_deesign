from django import forms
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalManyToManyField

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
    )
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail_deesign.base.blocks import BaseStreamBlock

#Import types of circuits to be designed.

#Power Electronics - DC/DC converter design:
from wagtail_deesign.circuit_designs.models import (
    DCDCDesignParamChoices, DCDCSelectedComponents, DCDCRecommendedComponents,
    DCDCOpenLoopAnalysisEquations, DCDCConverters
    )

@register_snippet
class Header(models.Model):
    """
    This provides editable text for the site header. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in design_center/templatetags/
    navigation_tags.py
    """
    header_text = BaseStreamBlock()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Header text"

    class Meta:
        verbose_name_plural = 'Header Text'

class DesignCenter(Page):
    """
    Detail view for a specific design.
    """

    content_panels = Page.content_panels + [
        FieldPanel('dcdc_design', classname="full"),
        MultiFieldPanel(
            [
                InlinePanel(DCDCConverters, "dc_dc_design", label="DC/DC Converter Design"),
            ],
            heading="DC/DC Converter Analysis",
            classname="collapsible collapsed"
        ),
        FieldPanel('analog_design', classname="full"),
        FieldPanel('fpga_design', classname="full"),
        ImageChooserPanel('circuit_image'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

class DCDCDesign(Page):
    circuit_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('dcdc_design', classname="full"),
        MultiFieldPanel(
            [
                InlinePanel(DCDCConverters, "dc_dc_design", label="DC/DC Converter Design"),
            ],
            heading="DC/DC Converter Analysis",
            classname="collapsible collapsed"
        ),
        FieldPanel('analog_design', classname="full"),
        FieldPanel('fpga_design', classname="full"),
        ImageChooserPanel('circuit_image'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
