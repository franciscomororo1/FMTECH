from django import forms
from .models import Cliente, Equipamento, OrdemServico, Receita

# ===============================
# FORM BASE
# ===============================

class BaseBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select border border-secondary'
                })

            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control border border-secondary',
                    'rows': 3
                })

            else:
                field.widget.attrs.update({
                    'class': 'form-control border border-secondary'
                })

# ===============================
# FORM DE CLIENTE
# ===============================
class ClienteForm(BaseBootstrapForm):
    class Meta:
        model = Cliente
        fields = '__all__'


# ===============================
# FORM DE EQUIPAMENTO
# ===============================
class EquipamentoForm(BaseBootstrapForm):
    class Meta:
        model = Equipamento
        fields = '__all__'


# ===============================
# FORM DE ORDEM DE SERVIÇO
# ===============================
class OrdemServicoForm(BaseBootstrapForm):
    class Meta:
        model = OrdemServico
        fields = [
            'equipamento',
            'tecnico',
            'status',
            'defeito_relatado',
            'diagnostico',
            'solucao',
            'valor_servico',
        ]

# ===============================
# FORM DE RECEITA
# ===============================

class ReceitaForm(BaseBootstrapForm):
    class Meta:
        model = Receita
        fields = [
            'ordem_servico',
            'descricao',
            'valor',
            'data_recebimento',
            'metodo_pagamento',
            'status_pagamento',
        ]

        widgets = {
            'ordem_servico': forms.Select(),
            'descricao': forms.TextInput(),
            'valor': forms.NumberInput(),
            'data_recebimento': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'metodo_pagamento': forms.TextInput(),
            'status_pagamento': forms.TextInput(),
        }
