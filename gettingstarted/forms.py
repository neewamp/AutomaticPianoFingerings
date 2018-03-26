from django import forms

from uploads.core.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

# from django import forms
# from .validator import FileExtensionValidator


# class DocumentForm(forms.Form):
#     docfile = forms.FileField(label='Choose a MusicXML file to annotate')
