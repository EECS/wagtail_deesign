from django import forms
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
    )
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .units import UNITS_CHOICES
from .base.blocks import BaseStreamBlock

#Import design center to 
from wagtail_deesign.design_center.models import DesignCenter

########################################################
## Structure of the models in this design are as follows:
## 1. Power Electronics (PowerElectronics)
##  2. Switch-Mode Power Supplies (SMPS)
##      3. Design parameter choices (DCDCDesignParamChoices)
##          4. Selected components for DCDC Analysis (DCDCSelectedComponents)
##          5. Recommended components for DCDC Design (DCDCRecommendedComponents)
##          6. DC/DC Open Loop Analysis Equations (DCDCOpenLoopAnalysisEquations)
##          7. DC/DC Converters (DCDCConverters)
#######################################################

@register_snippet
class PowerElectronics(models.Model):
    """
    A Django model to store types of power electronic circuits to design.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/circuit_designs/powerelectronics/).
    """
    POWER_ELECTRONIC_CIRCUIT_TYPES = [
        ("SMPS", "Switch-Mode Power Supplies")
    ]

    name = models.CharField(max_length=500, help_text="Enter the name of the type of power electronic circuit to be analyzed.", choices=POWER_ELECTRONIC_CIRCUIT_TYPES)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
    
    class Meta:
        verbose_name_plural = "Power Electronics"

@register_snippet
class SMPS(models.Model):
    """
    A Django model to store types of switch-mode power supplies circuits to design.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/circuit_designs/smps/).
    """

    SMPS_TYPES = [
        ("DCDC", "DC-DC Converters")
    ]

    name = models.CharField(max_length=200, help_text="Enter the name of the type of SMPS circuit to be stored.", choices=SMPS_TYPES)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
    class Meta:
        verbose_name_plural = "Switch-Mode Power Supplies"

@register_snippet
class DCDCDesignParamChoices(models.Model):
    """
    A Django model to store types of dc/dc design parameters.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/circuit_designs/dcdcdesignparamchoices/).
    """

    params = models.CharField(max_length = 100, help_text="Parameter for design, e.g. Switching Frequency.")
    units = models.CharField(max_length = 100, help_text="Unit for this parameter, e.g. kHz. All frequencies at this time are assumed in kHz.")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.params
        
    def __unicode__(self):
        return self.params

    class Meta:
        ordering = ['params']
        verbose_name = "DC/DC Design Parameter"
        verbose_name_plural = "DC/DC Design Parameters"

@register_snippet
class DCDCSelectedComponents(models.Model):
    """
    A Django model to store selected DC/DC components for design.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/circuit_designs/dcdcselectedcomponents/).
    """

    selected_components_for_analysis = models.CharField(max_length = 100, help_text="Selected components for DC/DC design, e.g. output capacitor.")
    units = models.CharField(max_length = 100, help_text="Selected components for DC/DC design, e.g. output capacitor.", choices=UNITS_CHOICES)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.selected_components_for_analysis

    class Meta:
        ordering = ['selected_components_for_analysis']
        verbose_name = "DC/DC Selected Component"
        verbose_name_plural = "DC/DC Selected Components"

@register_snippet
class DCDCRecommendedComponents(models.Model):
    """
    A Django model to store recommended components in a DC/DC converter design.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/circuit_designs/dcdcrecommendedcomponents/).
    """
    circuit_name = models.CharField(max_length=200, help_text="Enter the name of this circuit in the admin page.")
    component_name = models.CharField(max_length=200, help_text="Enter the name of this component in the admin page.")
    equation = models.TextField(max_length=5000, help_text="Enter the equation used to generate this recommended component.")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.circuit_name + " " + self.component_name

    class Meta:
        ordering = ['components']
        verbose_name = "DC/DC Recommended Component"
        verbose_name_plural = "DC/DC Recommended Components"

@register_snippet
class DCDCOpenLoopAnalysisEquations(models.Model):
    """
    A Django model to store open loop analysis equations for DC/DC converters.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/circuit_designs/dcdcopenloopanalysisequations/).
    """
    equation_name = models.CharField(max_length = 200, help_text="Enter the name to which this equation applies. E.g. Buck Converter Efficiency")
    equation = models.TextField(max_length=1000, help_text="Enter the equation to be used to analyze the converter.", default=str(1))
    units = models.CharField(max_length = 200, help_text="Enter the units of the resulting equation.", default=str(1))

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.equation_name

    class Meta:
        ordering = ['circuit_url']
        verbose_name = "DC/DC Analysis Equation"
        verbose_name_plural = "DC/DC Open-Loop Analysis Equations"

@register_snippet
class DCDCConverters(models.Model):
    """
    A Django model to store Dc/DC converter designs.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/circuit_designs/dcdcconverters/).
    """

    #Tie the DCDCConverters class to the design center page.
    dcdc_page = ParentalKey("DCDCDesign", related_name="dc_dc_converter")

    DCDC_TYPES = [
        ("CCM", "Continuous Conduction Mode")
    ]

    pe_circuit_type = models.ForeignKey(PowerElectronics, on_delete=models.CASCADE)

    smps_circuit_type = models.ForeignKey(SMPS, on_delete=models.CASCADE)

    dcdc_type = models.CharField(max_length=200, help_text="Enter the type of DC-DC converter to be modeled.", choices=DCDC_TYPES)

    name = models.CharField(max_length=200, help_text="Enter the name of this converter in the admin page.")

    description = BaseStreamBlock()

    design_params = ParentalKey('DCDCDesignParamChoices', related_name="design_params")

    recommended_components = ParentalKey('DCDCRecommendedComponents', related_name="rec_components")

    selected_components = ParentalKey('DCDCSelectedComponents', related_name="sel_components")

    open_loop_analysis_equations = ParentalKey('DCDCOpenLoopAnalysisEquations', related_name="open_loop_analysis")

    #Open loop bode plots of the converter.
    input_output_transfer = models.TextField(max_length=5000, help_text="Enter the input to output transfer function of the converter.")
    input_impedance = models.TextField(max_length=5000, help_text="Enter the input impedance of the converter.")
    output_impedance = models.TextField(max_length=5000, help_text="Enter the output impedance of the converter.")
    duty_output_transfer = models.TextField(max_length=5000, help_text="Enter the duty to output transfer function of the converter.")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.dcdc_type+ " " + self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "DC/DC Converter"
        verbose_name_plural = "DC/DC Converters"
