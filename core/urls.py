from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    # CLIENTES
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/excluir/', views.cliente_excluir, name='cliente_excluir'),
    
    # EQUIPAMENTOS
    path('equipamentos/', views.equipamento_lista, name='equipamento_lista'),
    path('equipamentos/novo/', views.equipamento_novo, name='equipamento_novo'),
    path('equipamentos/<int:pk>/editar/', views.equipamento_editar, name='equipamento_editar'),
    path('equipamentos/<int:pk>/excluir/', views.equipamento_excluir, name='equipamento_excluir'),

    # ORDEM DE SERVIÇO
    path('ordens/', views.os_lista, name='os_lista'),
    path('ordens/nova/', views.os_nova, name='os_nova'),
    path('ordens/<int:pk>/editar/', views.os_editar, name='os_editar'),
    path('ordens/<int:pk>/excluir/', views.os_excluir, name='os_excluir'),

    # RECEITAS
    path('receitas/', views.receita_lista, name='receita_lista'),
    path('receitas/nova/', views.receita_nova, name='receita_nova'),
    path('receitas/<int:pk>/editar/', views.receita_editar, name='receita_editar'),
    path('receitas/<int:pk>/excluir/', views.receita_excluir, name='receita_excluir'),

    # DASHBOARD
    path('', views.dashboard, name='dashboard'),



]
