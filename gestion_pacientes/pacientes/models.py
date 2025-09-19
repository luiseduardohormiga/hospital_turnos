from django.db import models

PRIORIDADES = {
    "Nivel 1: Prioridad muy alta": 1, #roja
    "Nivel 2: Prioridad alta": 2, # naranja
    "Nivel 3: Prioridad media": 3, # amarilla
    "Nivel 4: Prioridad baja": 4, # verde
    "Nivel 4: Prioridad muy baja": 5, # azul
}

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)

    tipo_documento = models.CharField(
        max_length=20,
        choices=[
            ("CC", "Cédula de Ciudadanía"),
            ("TI", "Tarjeta de Identidad"),
            ("RC", "Registro Civil"),
            ("CE", "Cédula de Extranjería"),
            ("PAS", "Pasaporte"),
        ],
        default="CC"
    )

    numero_documento = models.CharField(max_length=20, unique=True)

    prioridad = models.CharField(
        max_length=20,
        choices=[
            # ("normal", "Normal"),
            # ("adulto_mayor", "Adulto Mayor"),
            # ("embarazo", "Embarazo"),
            # ("urgencia", "Urgencia"),
            ("nivel_1", "Nivel 1: Prioridad muy alta"),
            ("nivel_2", "Nivel 2: Prioridad alta"),
            ("nivel_3", "Nivel 3: Prioridad media"),
            ("nivel_4", "Nivel 4: Prioridad baja"),
            ("nivel_5", "Nivel 4: Prioridad muy baja"),
        ],
        default="normal"
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def prioridad_valor(self):
        PRIORIDADES = {
            "Nivel 1: Prioridad muy alta": 1,
            "Nivel 2: Prioridad alta": 2,
            "Nivel 3: Prioridad media": 3,
            "Nivel 4: Prioridad baja": 4,
            "Nivel 4: Prioridad muy baja": 5,
        }
        return PRIORIDADES.get(self.prioridad, 99)

    def __str__(self):
        return f"{self.nombre} - {self.tipo_documento} {self.numero_documento} ({self.get_prioridad_display()})"

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
