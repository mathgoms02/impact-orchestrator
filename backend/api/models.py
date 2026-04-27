from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    CHOICES_TIPO = (
        ('VOLUNTARIO', 'Voluntário'),
        ('ONG', 'Instituição'),
    )
    user = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=CHOICES_TIPO)

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"

class Voluntario(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    habilidades = models.TextField()
    disponibilidade = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)

class Crise(models.Model):
    titulo = models.CharField(max_length=200)
    descricao_bruta = models.TextField()
    analise_ia = models.TextField(null=True, blank=True)
    ativa = models.BooleanField(default=True)
    data_registro = models.DateTimeField(auto_now_add=True)