from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as loginDjango
from django.contrib.auth.decorators import login_required

from estoque_app.forms import *
from estoque_app.models import *

# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request, 'index.html')

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'authentication/register.html')
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = User.objects.filter(email=email).first()
        if user:
            return HttpResponse('Já existe um usuário com este e-mail.')
       
        novo_usuario = User.objects.create_user(email=email, password=senha, first_name=nome, username=email)
        novo_usuario.save()

        return redirect('/login')
    

def login(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    else:
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(username=email, password=senha)

        if user:
            loginDjango(request, user)
            return redirect('index')
        else:
            return HttpResponse('E-mail ou senha inválidas')
        
        
#CRUD CATEGORIA ==================================================================================
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('index')
    else:
        form = CategoriaForm() 
    
    return render(request, 'categoria/adicionar_categoria.html', {'form': form})

def listar_categorias(request):
    categorias = Categoria.objects.all() 
    return render(request, 'categoria/listar_categorias.html', {'categorias': categorias})

def editar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'categoria/editar_categoria.html', {
        'form': form,
        'categoria': categoria
    })

    
def deletar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    
    if request.method == 'POST':
        categoria.delete() 
        return redirect('listar_categorias')
    
    return render(request, 'categoria/deletar_categoria.html', {'categoria': categoria})
#CRUD PRODUTO ==================================================================================

def adicionar_bem(request):
    if request.method == 'POST':
        form = BemForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('index')
    else:
        form = BemForm()  
    
    return render(request, 'bem/adicionar_bem.html', {'form': form})

def listar_bems(request):
    query = request.GET.get('q')
    if query:
        bems = Bem.objects.filter(nome__icontains=query)
    else:
        bems = Bem.objects.all()

    return render(request, 'bem/listar_bems.html', {'bems': bems})
def editar_bem(request, id_bem):
    bem = get_object_or_404(Bem, id_bem=id_bem)
    
    if request.method == 'POST':
        form = BemForm(request.POST, instance=bem)
        if form.is_valid():
            form.save()
            return redirect('listar_bems')
    else:
        form = BemForm(instance=bem)
    
    return render(request, 'bem/editar_bem.html', {'form': form, 'bem': bem})

def deletar_bem(request, id_bem):
    bem = get_object_or_404(Bem, id_bem=id_bem)
    
    if request.method == 'POST':
        bem.delete() 
        return redirect('listar_bems')
    
    return render(request, 'bem/deletar_bem.html', {'bem': bem})
#CRUD FORNECEDOR ==================================================================================
def adicionar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('index')
    else:
        form = FornecedorForm() 
    
    return render(request, 'fornecedor/adicionar_fornecedor.html', {'form': form})

def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'fornecedor/listar_fornecedores.html', {'fornecedores': fornecedores})

# Editar Fornecedor
def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)

    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('listar_fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)

    return render(request, 'fornecedor/editar_fornecedor.html', {
        'form': form,
        'fornecedor': fornecedor
    })

# Deletar Fornecedor
def deletar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)

    if request.method == 'POST':
        fornecedor.delete()
        return redirect('listar_fornecedores')

    return render(request, 'fornecedor/deletar_fornecedor.html', {'fornecedor': fornecedor})
#CRUD MOVIMENTAÇÃO DO ESTOQUE ==================================================================================
def adicionar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.save() 
            return redirect('listar_movimentacoes')
    else:
        form = MovimentacaoForm()
    
    return render(request, 'movimentacao/adicionar_movimentacao.html', {'form': form})


def listar_movimentacoes(request):
    movimentacoes = Movimentacao.objects.select_related('produto').all()
    return render(request, 'movimentacao/listar_movimentacoes.html', {'movimentacoes': movimentacoes})

def editar_movimentacao(request, id):
    movimentacao = get_object_or_404(Movimentacao, id_movimentacao=id)
    
    if request.method == 'POST':
        form = Movimentacao(request.POST, instance=movimentacao)
        if form.is_valid():
            form.save()
            return redirect('listar_movimentacoes')
    else:
        form = Movimentacao(instance=movimentacao)
    
    return render(request, 'movimentacao/editar_movimentacao.html', {
        'form': form,
        'movimentacao': movimentacao
    })
    
def deletar_movimentacao(request, id):
    movimentacao = get_object_or_404(Movimentacao, id_movimentacao=id)
    
    if request.method == 'POST':
        movimentacao.delete()
        return redirect('listar_movimentacoes')
    
    return render(request, 'movimentacao/deletar_movimentacao.html', {'movimentacao': movimentacao})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Departamento, RFID
from .forms import DepartamentoForm, RFIDForm

# CRUD DEPARTAMENTO ==================================================================================

def adicionar_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_departamentos')
    else:
        form = DepartamentoForm()
    
    return render(request, 'departamento/adicionar_departamento.html', {'form': form})


def listar_departamentos(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamento/listar_departamentos.html', {'departamentos': departamentos})


def editar_departamento(request, id):
    departamento = get_object_or_404(Departamento, id=id)
    
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('listar_departamentos')
    else:
        form = DepartamentoForm(instance=departamento)
    
    return render(request, 'departamento/editar_departamento.html', {
        'form': form,
        'departamento': departamento
    })


def deletar_departamento(request, id):
    departamento = get_object_or_404(Departamento, id=id)
    
    if request.method == 'POST':
        departamento.delete()
        return redirect('listar_departamentos')
    
    return render(request, 'departamento/deletar_departamento.html', {'departamento': departamento})

# CRUD RFID ==================================================================================

def adicionar_rfid(request):
    if request.method == 'POST':
        form = RFIDForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_rfid')
    else:
        form = RFIDForm()
    
    return render(request, 'rfid/adicionar_rfid.html', {'form': form})


def listar_rfid(request):
    rfids = RFID.objects.select_related('bem').all()
    return render(request, 'rfid/listar_rfid.html', {'rfids': rfids})


def editar_rfid(request, id):
    rfid = get_object_or_404(RFID, id=id)
    
    if request.method == 'POST':
        form = RFIDForm(request.POST, instance=rfid)
        if form.is_valid():
            form.save()
            return redirect('listar_rfid')
    else:
        form = RFIDForm(instance=rfid)
    
    return render(request, 'rfid/editar_rfid.html', {
        'form': form,
        'rfid': rfid
    })


def deletar_rfid(request, id):
    rfid = get_object_or_404(RFID, id=id)
    
    if request.method == 'POST':
        rfid.delete()
        return redirect('listar_rfid')
    
    return render(request, 'rfid/deletar_rfid.html', {'rfid': rfid})

def logout_view(request):
    logout(request)
    return redirect('login')
