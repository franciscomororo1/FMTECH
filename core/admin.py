from django.contrib import admin
from .models import (
    Cliente,
    Equipamento,
    Tecnico,
    OrdemServico,
    Servico,
    OrdemServicoServico,
    Receita,
    Despesa,
)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'data_cadastro')
    search_fields = ('nome', 'cpf_cnpj')


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo', 'marca', 'modelo')
    list_filter = ('tipo',)
    search_fields = ('marca', 'modelo', 'numero_serie')


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero_os', 'equipamento', 'tecnico', 'status', 'data_abertura')
    list_filter = ('status', 'data_abertura')
    search_fields = ('numero_os', 'equipamento__cliente__nome')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor')
    search_fields = ('descricao',)


@admin.register(OrdemServicoServico)
class OrdemServicoServicoAdmin(admin.ModelAdmin):
    list_display = ('ordem_servico', 'servico', 'quantidade')


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data_recebimento', 'status_pagamento')
    list_filter = ('status_pagamento',)
    search_fields = ('descricao',)


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data_pagamento', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('descricao',)

