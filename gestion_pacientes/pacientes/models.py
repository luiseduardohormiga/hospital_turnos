from django.db import models

PRIORIDADES = {
    "urgencia": 1,
    "embarazo": 2,
    "adulto_mayor": 3,
    "normal": 4,
}

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    prioridad = models.CharField(
        max_length=20,
        choices=[
            ("normal", "Normal"),
            ("adulto_mayor", "Adulto Mayor"),
            ("embarazo", "Embarazo"),
            ("urgencia", "Urgencia"),
        ],
        default="normal"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def prioridad_valor(self):
        PRIORIDADES = {
            "urgencia": 1,
            "embarazo": 2,
            "adulto_mayor": 3,
            "normal": 4,
        }
        return PRIORIDADES.get(self.prioridad, 99)

    def __str__(self):
        return f"{self.nombre} ({self.get_prioridad_display()})"


class Turno(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    numero_turno = models.PositiveIntegerField(unique=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("en_atencion", "En Atención"),
            ("atendido", "Atendido"),
        ],
        default="pendiente"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Turno {self.numero_turno} - {self.paciente.nombre} ({self.estado})"
