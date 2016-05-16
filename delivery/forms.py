from django import forms
from .models import Family
from django.utils.html import escape

def add_class_label_tag(original_function):
    """Adds the 'required' CSS class and an asterisks to required field labels."""
    def required_label_tag(self, contents=None, attrs=None, label_suffix=None):
        contents = contents or escape(self.label)
        attrs = {'class': 'uk-form-label'}
        return original_function(self, contents, attrs, label_suffix)
    return required_label_tag

def decorate_bound_field():
  from django.forms.forms import BoundField
  BoundField.label_tag = add_class_label_tag(BoundField.label_tag)

class FamilyForm(forms.Form):
    name = forms.CharField(label='Nom du Foyer', max_length=100)
    username = forms.CharField(label='Nom d\'utilisateur', max_length=100)
    email = forms.EmailField(label='Email')
    tel = forms.CharField(label='Telephone (non obligatoire)', max_length=100, required=False)

decorate_bound_field()
