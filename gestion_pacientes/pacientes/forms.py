from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nombre", "prioridad"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "prioridad": forms.Select(attrs={"class": "form-control"}),
        }
