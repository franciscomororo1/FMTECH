from django.contrib import admin
from .models import Cliente, Equipamento, Tecnico, OrdemServico


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email')


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'cliente')


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_os',
        'get_cliente',
        'status',
        'data_abertura',
    )

    def get_cliente(self, obj):
        return obj.equipamento.cliente

    get_cliente.short_description = 'Cliente'
