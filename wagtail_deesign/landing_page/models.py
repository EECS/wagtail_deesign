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
#from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel

from .base.blocks import BaseStreamBlock

class LandingPage(Page):
    """
    Detail view for a specific bread
    """
    title = models.TextField(
        help_text='Hook text to draw the reader into the site and serve as the title text of the front page.',
        blank=True)

    title_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    subtitle_text = models.TextField(
        help_text='Hook text to draw the reader into the site that is below the site image.',
        blank=True)

    content_description = StreamField(
        BaseStreamBlock(), verbose_name="Description of content in the design center.", blank=True
    )


    # We include related_name='+' to avoid name collisions on relationships.
    # e.g. there are two FooPage models in two different apps,
    # and they both have a FK to bread_type, they'll both try to create a
    # relationship called `foopage_objects` that will throw a valueError on
    # collision.
    #bread_type = models.ForeignKey(
    #    'breads.BreadType',
    #    null=True,
    #    blank=True,
    #    on_delete=models.SET_NULL,
    #    related_name='+'
    #)
    #ingredients = ParentalManyToManyField('BreadIngredient', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('title', classname="full"),
        ImageChooserPanel('title_image'),
        FieldPanel('subtitle_text', classname="full"),
        StreamFieldPanel('content_description'),
        #MultiFieldPanel(
        #    [
        #        FieldPanel(
        #            'ingredients',
        #            widget=forms.CheckboxSelectMultiple,
        #        ),
        #    ],
        #    heading="Additional Metadata",
        #    classname="collapsible collapsed"
        #),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('content_description'),
    ]

    #parent_page_types = ['BreadsIndexPage']
