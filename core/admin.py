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


# =========================
# CLIENTE
# =========================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'data_cadastro')
    search_fields = ('nome', 'cpf_cnpj', 'email')
    list_filter = ('data_cadastro',)
    ordering = ('nome',)


# =========================
# EQUIPAMENTO
# =========================
@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo', 'marca', 'modelo', 'numero_serie')
    search_fields = ('marca', 'modelo', 'numero_serie', 'cliente__nome')
    list_filter = ('tipo',)
    autocomplete_fields = ('cliente',)


# =========================
# TÉCNICO
# =========================
@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)


# =========================
# ORDEM DE SERVIÇO
# =========================
@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_os',
        'get_cliente',
        'equipamento',
        'tecnico',
        'status',
        'data_abertura',
        'data_fechamento',
        'valor_servico',
    )

    list_filter = ('status', 'data_abertura', 'tecnico')
    search_fields = ('numero_os', 'equipamento__cliente__nome')
    date_hierarchy = 'data_abertura'
    autocomplete_fields = ('equipamento', 'tecnico')
    readonly_fields = ('numero_os', 'data_abertura')

    def get_cliente(self, obj):
        return obj.equipamento.cliente

    get_cliente.short_description = 'Cliente'


# =========================
# SERVIÇO
# =========================
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor')
    search_fields = ('descricao',)


# =========================
# SERVIÇOS DA ORDEM
# =========================
@admin.register(OrdemServicoServico)
class OrdemServicoServicoAdmin(admin.ModelAdmin):
    list_display = ('ordem_servico', 'servico', 'quantidade')
    autocomplete_fields = ('ordem_servico', 'servico')


# =========================
# RECEITA
# =========================
@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data_recebimento', 'status_pagamento')
    list_filter = ('status_pagamento', 'metodo_pagamento')
    autocomplete_fields = ('ordem_servico',)


# =========================
# DESPESA
# =========================
@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'valor',
        'data_despesa',
        'status',
    )

    list_filter = (
        'status',
        'data_despesa',
    )

    search_fields = (
        'descricao',
        'observacao',
    )