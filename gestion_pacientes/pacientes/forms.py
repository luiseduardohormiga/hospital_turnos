from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nombre", "tipo_documento", "numero_documento"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_documento": forms.Select(attrs={"class": "form-control"}),
            "numero_documento": forms.TextInput(attrs={"class": "form-control"}),
        }