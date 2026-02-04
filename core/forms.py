from django import forms
from .models import Cliente, Equipamento, OrdemServico, Receita, Despesa

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
# FORM DE ORDEM DE SERVIÇO COMPLETO
# ===============================

class OrdemServicoForm(BaseBootstrapForm):
    
    # ===============================
    # EQUIPAMENTO
    # ===============================
    
    equipamento = forms.ModelChoiceField(
        queryset=Equipamento.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )


    # ===============================
    # CLIENTE EXISTENTE
    # ===============================
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        label='Cliente existente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # ===============================
    # NOVO CLIENTE
    # ===============================
    cliente_nome = forms.CharField(required=False, label='Nome')
    cliente_cpf_cnpj = forms.CharField(required=False, label='CPF/CNPJ')
    cliente_telefone = forms.CharField(required=False, label='Telefone')
    cliente_email = forms.EmailField(required=False, label='Email')
    cliente_endereco = forms.CharField(required=False, label='Endereço')

    # ===============================
    # EQUIPAMENTO EXISTENTE
    # ===============================
    equipamento_existente = forms.ModelChoiceField(
        queryset=Equipamento.objects.all(),
        required=False,
        label='Equipamento existente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # ===============================
    # NOVO EQUIPAMENTO
    # ===============================
    tipo = forms.ChoiceField(
        choices=Equipamento.TIPO_CHOICES,
        required=False,
        label='Tipo'
    )

    marca = forms.CharField(required=False)
    modelo = forms.CharField(required=False)
    numero_serie = forms.CharField(required=False)

    descricao = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    # ===============================
    # META
    # ===============================
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

# ===============================
# FORM DE DESPESAS
# ===============================

class DespesaForm(BaseBootstrapForm):
    class Meta:
        model = Despesa
        fields = [
            'descricao',
            'valor',
            'data_despesa',
            'status',
            'observacao',
        ]

        widgets = {
            'descricao': forms.TextInput(),
            'valor': forms.NumberInput(),
            'data_despesa': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'status': forms.Select(),
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }

# ===============================
# FORM INLINE CLIENTE (OS)
# ===============================

class ClienteInlineForm(BaseBootstrapForm):
    class Meta:
        model = Cliente
        fields = [
            'nome',
            'cpf_cnpj',
            'telefone',
            'email',
            'endereco',
        ]


# ===============================
# FORM INLINE EQUIPAMENTO (OS)
# ===============================

class EquipamentoInlineForm(BaseBootstrapForm):
    class Meta:
        model = Equipamento
        fields = [
            'cliente',
            'tipo',
            'marca',
            'modelo',
            'numero_serie',
            'descricao',
        ]
