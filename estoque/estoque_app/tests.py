from django.test import TestCase, Client
from django.urls import reverse
from .models import Categoria, Departamento, Fornecedor, Bem, Movimentacao
from datetime import date

# ========== TESTES PARA MODELS ==========
class CategoriaModelTest(TestCase):
    def test_criacao_categoria(self):
        categoria = Categoria.objects.create(nome="Eletrônicos")
        self.assertEqual(str(categoria), "Eletrônicos")

    def test_nome_unico(self):
        Categoria.objects.create(nome="Móveis")
        with self.assertRaises(Exception):
            Categoria.objects.create(nome="Móveis")  # Deve dar erro porque é unique=True

class DepartamentoModelTest(TestCase):
    def test_criacao_departamento(self):
        departamento = Departamento.objects.create(nome="TI")
        self.assertEqual(str(departamento), "TI")

class FornecedorModelTest(TestCase):
    def test_criacao_fornecedor(self):
        fornecedor = Fornecedor.objects.create(nome="Tech Supplier", contato="123456789", email="tech@supplier.com")
        self.assertEqual(str(fornecedor), "Tech Supplier")

class BemModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.departamento = Departamento.objects.create(nome="TI")
        self.fornecedor = Fornecedor.objects.create(nome="Tech Supplier")

    def test_criacao_bem(self):
        bem = Bem.objects.create(
            nome="Notebook Dell",
            descricao="Notebook para trabalho",
            numero_patrimonio="NB-001",
            categoria=self.categoria,
            departamento=self.departamento,
            fornecedor=self.fornecedor,
            data_aquisicao=date.today(),
            valor=4500.00,
            status="ativo"
        )
        self.assertEqual(str(bem), "Notebook Dell (NB-001)")

    def test_numero_patrimonio_unico(self):
        Bem.objects.create(nome="PC", numero_patrimonio="PC-123", data_aquisicao=date.today(), valor=3000.00)
        with self.assertRaises(Exception):
            Bem.objects.create(nome="Outro PC", numero_patrimonio="PC-123", data_aquisicao=date.today(), valor=3500.00)

class MovimentacaoModelTest(TestCase):
    def setUp(self):
        self.departamento_origem = Departamento.objects.create(nome="Almoxarifado")
        self.departamento_destino = Departamento.objects.create(nome="TI")
        self.bem = Bem.objects.create(nome="Monitor", numero_patrimonio="MON-001", data_aquisicao=date.today(), valor=1200.00)

    def test_criacao_movimentacao(self):
        movimentacao = Movimentacao.objects.create(
            bem=self.bem,
            origem=self.departamento_origem,
            destino=self.departamento_destino,
            responsavel="Carlos"
        )
        self.assertEqual(str(movimentacao), "Monitor de Almoxarifado para TI")

# ========== TESTES PARA VIEWS ==========
class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.departamento = Departamento.objects.create(nome="TI")
        self.fornecedor = Fornecedor.objects.create(nome="Tech Supplier")
        self.bem = Bem.objects.create(
            nome="Notebook",
            numero_patrimonio="NB-123",
            categoria=self.categoria,
            departamento=self.departamento,
            fornecedor=self.fornecedor,
            data_aquisicao=date.today(),
            valor=5000.00,
            status="ativo"
        )

    def test_listar_categorias(self):
        response = self.client.get(reverse('listar_categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eletrônicos")

    def test_adicionar_categoria(self):
        response = self.client.post(reverse('adicionar_categoria'), {'nome': 'Móveis'})
        self.assertEqual(response.status_code, 302)  # Deve redirecionar após criar
        self.assertTrue(Categoria.objects.filter(nome="Móveis").exists())

    def test_listar_bens(self):
        response = self.client.get(reverse('listar_bems'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Notebook")

    def test_editar_bem(self):
        response = self.client.post(reverse('editar_bem', kwargs={'id': self.bem.id}), {
            'nome': 'Notebook Atualizado',
            'numero_patrimonio': 'NB-123',
            'categoria': self.categoria.id,
            'departamento': self.departamento.id,
            'fornecedor': self.fornecedor.id,
            'data_aquisicao': date.today(),
            'valor': 5500.00,
            'status': 'ativo'
        })
        self.bem.refresh_from_db()
        self.assertEqual(self.bem.nome, "Notebook Atualizado")

    def test_deletar_bem(self):
        response = self.client.post(reverse('deletar_bem', kwargs={'id': self.bem.id}))
        self.assertEqual(response.status_code, 302)  # Deve redirecionar após deletar
        self.assertFalse(Bem.objects.filter(id=self.bem.id).exists())



# ========== TESTES PARA FORMS ==========
from .forms import CategoriaForm, BemForm

class FormTest(TestCase):
    def test_form_categoria_valido(self):
        form = CategoriaForm(data={'nome': 'Eletrodomésticos'})
        self.assertTrue(form.is_valid())

    def test_form_categoria_invalido(self):
        form = CategoriaForm(data={'nome': ''})
        self.assertFalse(form.is_valid())

    def test_form_bem_valido(self):
        categoria = Categoria.objects.create(nome="Móveis")
        departamento = Departamento.objects.create(nome="Administração")
        fornecedor = Fornecedor.objects.create(nome="Fornecedor XYZ")

        form = BemForm(data={
            'nome': 'Cadeira de Escritório',
            'descricao': 'Cadeira confortável',
            'numero_patrimonio': 'CAD-001',
            'categoria': categoria.id,
            'departamento': departamento.id,
            'fornecedor': fornecedor.id,
            'data_aquisicao': date.today(),
            'valor': 1200.00,
            'status': 'ativo'
        })
        self.assertTrue(form.is_valid())

    def test_form_bem_invalido(self):
        form = BemForm(data={
            'nome': '',
            'descricao': 'Sem nome',
            'numero_patrimonio': '',
            'data_aquisicao': date.today(),
            'valor': 0.00,
            'status': 'ativo'
        })
        self.assertFalse(form.is_valid())
