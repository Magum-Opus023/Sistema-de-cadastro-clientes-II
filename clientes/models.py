from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    aniversario = models.CharField(max_length=5, help_text='Formato: dd/mm', null=True, blank=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clientes")

    data_criacao = models.DateTimeField(auto_now_add=True)

    PAGAMENTO_CHOICES = [
        ('À Vista', 'À Vista'),
        ('PIX', 'PIX'),
        ('Boleto', 'Boleto'),
        ('Cartão de Crédito', 'Cartão de Crédito'),
        ('Cartão de Débito', 'Cartão de Débito'),
        ('Transferência Bancária', 'Transferência Bancária'),
        ('Outro', 'Outro'),
    ]

    pagamento = models.CharField(
        max_length=60,
        choices=PAGAMENTO_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome