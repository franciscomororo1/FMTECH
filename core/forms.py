from django import forms
from .models import Cliente, Equipamento, OrdemServico


# =========================
# FORM DE CLIENTE
# =========================
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(),
            'cpf_cnpj': forms.TextInput(),
            'telefone': forms.TextInput(),
            'email': forms.EmailInput(),
            'endereco': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control border border-secondary'
            })


# =========================
# FORM DE EQUIPAMENTO
# =========================
class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(),
            'tipo': forms.Select(),
            'marca': forms.TextInput(),
            'modelo': forms.TextInput(),
            'numero_serie': forms.TextInput(),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select border border-secondary'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control border border-secondary'
                })


# =========================
# FORM DE ORDEM DE SERVIÇO
# =========================
class OrdemServicoForm(forms.ModelForm):
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
        widgets = {
            'equipamento': forms.Select(),
            'tecnico': forms.Select(),
            'status': forms.Select(),
            'defeito_relatado': forms.Textarea(attrs={'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'solucao': forms.Textarea(attrs={'rows': 3}),
            'valor_servico': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select border border-secondary'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control border border-secondary'
                })
