"""
IPython widgets compatibility layer

Provides IPython 3.x widgets when running in IPython 2.x. 
The style attributes are not supported, so the user interface looks somewhat 
ugly in IPython 2.x.
"""

from IPython.html import widgets
import IPython

if IPython.version_info >= (3, 0, 0):
    from IPython.html.widgets import (
        CallbackDispatcher, 
        Box, FlexBox, Tab,
        Button, ToggleButtons, Checkbox, 
        IntText, IntSlider, BoundedIntText, IntProgress, 
        FloatText, FloatSlider, BoundedFloatText,
        Dropdown, Select, 
        HTML, Textarea, 
        Widget, DOMWidget
    )
else:
    from IPython.html.widgets import (
        CallbackDispatcher, 
        ContainerWidget as Box, TabWidget as Tab,
        ButtonWidget as Button, ToggleButtonsWidget, CheckboxWidget as Checkbox, 
        IntSliderWidget as IntSlider, IntProgressWidget as IntProgress,
        FloatTextWidget as FloatText, FloatSliderWidget as FloatSlider, 
        BoundedFloatTextWidget as BoundedFloatText,
        DropdownWidget, SelectWidget, 
        HTMLWidget as HTML, TextareaWidget as Textarea,
        Widget, DOMWidget
    )
    import IPython.utils.traitlets as traitlets
    from functools import wraps
    
    class FlexBox(Box):
        def __init__(self, orientation='vertical', align='start', **kwargs):
            super(FlexBox, self).__init__(**kwargs)
            self.orientation = orientation
            self.align = align
            self.on_displayed(self._on_displayed)
        
        def _on_displayed(self, _):
            ''' set correct CSS classes '''
            if self.orientation == 'horizontal':
                self.remove_class('vbox')
                self.add_class('hbox')
            if self.align != 'start':
                self.add_class('align-' + self.align)
            
                
    class Select(SelectWidget):
        options = traitlets.Dict()
        
        @wraps(SelectWidget.__init__)
        def __init__(self, *args, **kwargs):
            if 'options' in kwargs:
                kwargs['values'] = kwargs.pop('options')
            super(Select, self).__init__(*args, **kwargs)
            traitlets.link((self, 'values'), (self, 'options'))

    class Dropdown(DropdownWidget):
        options = traitlets.Dict()
        
        @wraps(DropdownWidget.__init__)
        def __init__(self, *args, **kwargs):
            if 'options' in kwargs:
                kwargs['values'] = kwargs.pop('options')
            super(Dropdown, self).__init__(*args, **kwargs)
            traitlets.link((self, 'values'), (self, 'options'))
        
    class ToggleButtons(ToggleButtonsWidget):
        options = traitlets.Dict()
        
        @wraps(ToggleButtonsWidget.__init__)
        def __init__(self, *args, **kwargs):
            if 'options' in kwargs:
                kwargs['values'] = kwargs.pop('options')
            super(ToggleButtons, self).__init__(*args, **kwargs)
            traitlets.link((self, 'values'), (self, 'options'))

if hasattr(Widget, '__del__'):
    del Widget.__del__

def close_all():
    """Close all active widgets."""
    for widget in Widget.widgets.values():
        widget.close()