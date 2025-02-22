from django.db import models

# Create your models here.
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    nome = models.CharField(max_length=150)
    contato = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Bem(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    numero_patrimonio = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    data_aquisicao = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('ativo', 'Ativo'),
            ('manutencao', 'Em Manutenção'),
            ('baixado', 'Baixado'),
        ],
        default='ativo'
    )
    rfid = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.numero_patrimonio})"


class Movimentacao(models.Model):
    bem = models.ForeignKey(Bem, on_delete=models.CASCADE)
    origem = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, related_name='movimentacoes_origem')
    destino = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, related_name='movimentacoes_destino')
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    responsavel = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.bem.nome} de {self.origem} para {self.destino}"


