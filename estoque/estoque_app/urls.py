from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),

    # URLs para Categoria
    path('categoria/', views.listar_categorias, name='listar_categorias'),
    path('categoria/adicionar/', views.adicionar_categoria, name='adicionar_categoria'),
    path('categoria/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categoria/deletar/<int:id>/', views.deletar_categoria, name='deletar_categoria'),

    # URLs para Bem
    path('bem/', views.listar_bems, name='listar_bems'),
    path('bem/adicionar/', views.adicionar_bem, name='adicionar_bem'),
    path('bem/editar/<int:id>/', views.editar_bem, name='editar_bem'),
    path('bem/deletar/<int:id>/', views.deletar_bem, name='deletar_bem'),

    # URLs para Movimentação
    path('movimentacao/', views.listar_movimentacoes, name='listar_movimentacoes'),
    path('movimentacao/adicionar/', views.adicionar_movimentacao, name='adicionar_movimentacao'),
    path('movimentacao/editar/<int:id>/', views.editar_movimentacao, name='editar_movimentacao'),
    path('movimentacao/deletar/<int:id>/', views.deletar_movimentacao, name='deletar_movimentacao'),
    
    # URLs para Fornecedor
    path('fornecedor/', views.listar_fornecedores, name='listar_fornecedores'),
    path('fornecedor/adicionar/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('fornecedor/editar/<int:id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedor/deletar/<int:id>/', views.deletar_fornecedor, name='deletar_fornecedor'),

    # URLs para Departamento
    path('departamento/', views.listar_departamentos, name='listar_departamentos'),
    path('departamento/adicionar/', views.adicionar_departamento, name='adicionar_departamento'),
    path('departamento/editar/<int:id>/', views.editar_departamento, name='editar_departamento'),
    path('departamento/deletar/<int:id>/', views.deletar_departamento, name='deletar_departamento'),

    # URLs para RFID
    # path('rfid/', views.listar_rfid, name='listar_rfid'),
    # path('rfid/adicionar/', views.adicionar_rfid, name='adicionar_rfid'),
    # path('rfid/editar/<int:id>/', views.editar_rfid, name='editar_rfid'),
    # path('rfid/deletar/<int:id>/', views.deletar_rfid, name='deletar_rfid'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # URLs para redefinição de senha
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
