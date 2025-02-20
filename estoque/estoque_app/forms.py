from django import forms
from .models import Bem, Categoria, Departamento, Fornecedor, Movimentacao, RFID

class BemForm(forms.ModelForm):
    class Meta:
        model = Bem
        fields = ['nome', 'valor', 'descricao', 'departamento', 'categoria', 'fornecedor', 
                  'numero_patrimonio', 'data_aquisicao', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do bem'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'numero_patrimonio': forms.TextInput(attrs={'class': 'form-control'}),
            'data_aquisicao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'}),
        }

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do departamento'}),
        }

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'contato', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do fornecedor'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contato'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['bem', 'origem', 'destino', 'responsavel']
        widgets = {
            'bem': forms.Select(attrs={'class': 'form-select'}),
            'origem': forms.Select(attrs={'class': 'form-select'}),
            'destino': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsável'}),
        }
class RFIDForm(forms.ModelForm):
    class Meta:
        model = RFID
        fields = ['bem', 'tag_id']
        widgets = {
            'bem': forms.Select(attrs={'class': 'form-select'}),
            'tag_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código RFID'}),

        }
