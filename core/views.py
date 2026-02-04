from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .models import (
    Cliente,
    Equipamento,
    OrdemServico,
    Receita,
    Despesa,
)
from .forms import (
    ClienteForm,
    EquipamentoForm,
    OrdemServicoForm,
    ReceitaForm,
    DespesaForm,
    ClienteInlineForm,
    EquipamentoInlineForm,
)

# =========================
# CLIENTE
# =========================

@login_required
def cliente_lista(request):
    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'core/cliente/lista.html', {
        'clientes': clientes,
        'titulo': 'Clientes',
        'botao_label': '+ Novo Cliente',
        'botao_url': 'cliente_novo',
    })


@login_required
def cliente_novo(request):
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('cliente_lista')

    return render(request, 'core/cliente/form.html', {'form': form})


@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('cliente_lista')

    return render(request, 'core/cliente/form.html', {'form': form})


@login_required
def cliente_excluir(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('cliente_lista')

    return render(request, 'core/cliente/excluir.html', {'cliente': cliente})


# =========================
# EQUIPAMENTO
# =========================

@login_required
def equipamento_lista(request):
    equipamentos = Equipamento.objects.select_related('cliente').all()

    return render(request, 'core/equipamento/lista.html', {
        'equipamentos': equipamentos,
        'titulo': 'Equipamentos',
        'botao_label': '+ Novo Equipamento',
        'botao_url': 'equipamento_novo',
    })


@login_required
def equipamento_novo(request):
    form = EquipamentoForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Equipamento cadastrado com sucesso!')
        return redirect('equipamento_lista')

    return render(request, 'core/equipamento/form.html', {'form': form})


@login_required
def equipamento_editar(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    form = EquipamentoForm(request.POST or None, instance=equipamento)

    if form.is_valid():
        form.save()
        messages.success(request, 'Equipamento atualizado com sucesso!')
        return redirect('equipamento_lista')

    return render(request, 'core/equipamento/form.html', {'form': form})


@login_required
def equipamento_excluir(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)

    if request.method == 'POST':
        equipamento.delete()
        messages.success(request, 'Equipamento excluído com sucesso!')
        return redirect('equipamento_lista')

    return render(request, 'core/equipamento/excluir.html', {'equipamento': equipamento})


# =========================
# ORDEM DE SERVIÇO
# =========================

@login_required
def os_lista(request):
    ordens = OrdemServico.objects.select_related(
        'equipamento',
        'tecnico'
    ).order_by('-data_abertura')

    return render(request, 'core/os/lista.html', {
        'ordens': ordens,
        'titulo': 'Ordens de Serviço',
        'botao_label': '+ Nova OS',
        'botao_url': 'os_nova',
    })



@login_required
def os_nova(request):

    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)

        if form.is_valid():

            # ===============================
            # CLIENTE
            # ===============================
            cliente = form.cleaned_data.get('cliente')

            if not cliente:
                nome = form.cleaned_data.get('cliente_nome')

                if nome:
                    cliente = Cliente.objects.create(
                        nome=nome,
                        cpf_cnpj=form.cleaned_data.get('cliente_cpf_cnpj'),
                        telefone=form.cleaned_data.get('cliente_telefone'),
                        email=form.cleaned_data.get('cliente_email'),
                        endereco=form.cleaned_data.get('cliente_endereco'),
                    )
                else:
                    form.add_error(
                        'cliente',
                        'Selecione ou cadastre um cliente.'
                    )
                    return render(
                        request,
                        'core/os/form.html',
                        {'form': form}
                    )

            # ===============================
            # EQUIPAMENTO
            # ===============================
            equipamento = form.cleaned_data.get(
                'equipamento_existente'
            )

            if not equipamento:
                tipo = form.cleaned_data.get('tipo')

                if tipo:
                    equipamento = Equipamento.objects.create(
                        cliente=cliente,
                        tipo=tipo,
                        marca=form.cleaned_data.get('marca'),
                        modelo=form.cleaned_data.get('modelo'),
                        numero_serie=form.cleaned_data.get('numero_serie'),
                        descricao=form.cleaned_data.get('descricao'),
                    )
                else:
                    form.add_error(
                        'equipamento_existente',
                        'Selecione ou cadastre um equipamento.'
                    )
                    return render(
                        request,
                        'core/os/form.html',
                        {'form': form}
                    )

            # ===============================
            # SALVA OS
            # ===============================
            os = form.save(commit=False)
            os.equipamento = equipamento
            os.save()

            # ===============================
            # REDIRECIONA PRA LISTA
            # ===============================
            return redirect('os_lista')

    else:
        form = OrdemServicoForm()

    return render(
        request,
        'core/os/form.html',
        {'form': form}
    )
  

@login_required
def os_print(request, pk):

    os = OrdemServico.objects.get(pk=pk)

    return render(
        request,
        'core/os/print.html',
        {'os': os}
    )


@login_required
def os_editar(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)
    form = OrdemServicoForm(request.POST or None, instance=os)

    if form.is_valid():
        form.save()
        messages.success(
            request,
            f'Ordem de Serviço {os.numero_os} atualizada!'
        )
        return redirect('os_lista')

    return render(request, 'core/os/form.html', {
        'form': form,
        'os': os
    })


@login_required
def os_excluir(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':
        numero = os.numero_os
        os.delete()
        messages.success(
            request,
            f'Ordem de Serviço {numero} excluída!'
        )
        return redirect('os_lista')

    return render(request, 'core/os/excluir.html', {'os': os})


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    hoje = date.today()

    total_clientes = Cliente.objects.count()

    os_abertas = OrdemServico.objects.filter(
        status__in=[
            OrdemServico.STATUS_ABERTA,
            OrdemServico.STATUS_ANDAMENTO,
            OrdemServico.STATUS_AGUARDANDO,
        ]
    ).count()

    os_concluidas = OrdemServico.objects.filter(
        status=OrdemServico.STATUS_CONCLUIDA
    ).count()

    receitas_mes = Receita.objects.filter(
        data_recebimento__year=hoje.year,
        data_recebimento__month=hoje.month
    ).aggregate(total=Sum('valor'))['total'] or 0

    despesas_mes = Despesa.objects.filter(
        data_despesa__year=hoje.year,
        data_despesa__month=hoje.month
    ).aggregate(total=Sum('valor'))['total'] or 0

    saldo_mes = receitas_mes - despesas_mes

    ultimas_os = OrdemServico.objects.select_related(
        'equipamento',
        'equipamento__cliente'
    ).order_by('-data_abertura')[:5]

    ultimas_despesas = Despesa.objects.order_by('-data_despesa')[:5]

    return render(request, 'core/dashboard.html', {
        'total_clientes': total_clientes,
        'os_abertas': os_abertas,
        'os_concluidas': os_concluidas,
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'saldo_mes': saldo_mes,
        'ultimas_os': ultimas_os,
        'ultimas_despesas': ultimas_despesas,
    })


# =========================
# RECEITAS
# =========================

@login_required
def receita_lista(request):
    receitas = Receita.objects.select_related(
        'ordem_servico'
    ).order_by('-data_recebimento')

    return render(request, 'core/receita/lista.html', {
        'receitas': receitas,
        'titulo': 'Receitas',
        'botao_label': '+ Nova Receita',
        'botao_url': 'receita_nova',
    })


@login_required
def receita_nova(request):
    form = ReceitaForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Receita cadastrada com sucesso!')
        return redirect('receita_lista')

    return render(request, 'core/receita/form.html', {
        'form': form,
        'titulo': 'Nova Receita'
    })


@login_required
def receita_editar(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    form = ReceitaForm(request.POST or None, instance=receita)

    if form.is_valid():
        form.save()
        messages.success(request, 'Receita atualizada com sucesso!')
        return redirect('receita_lista')

    return render(request, 'core/receita/form.html', {
        'form': form,
        'titulo': 'Editar Receita'
    })


@login_required
def receita_excluir(request, pk):
    receita = get_object_or_404(Receita, pk=pk)

    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita excluída com sucesso!')
        return redirect('receita_lista')

    return render(request, 'core/receita/excluir.html', {
        'receita': receita
    })


# =========================
# DESPESAS
# =========================

@login_required
def despesa_lista(request):
    despesas = Despesa.objects.order_by('-data_despesa')

    return render(request, 'core/despesa/lista.html', {
        'despesas': despesas,
        'titulo': 'Despesas',
        'botao_label': '+ Nova Despesa',
        'botao_url': 'despesa_nova',
    })


@login_required
def despesa_nova(request):
    form = DespesaForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Despesa cadastrada com sucesso!')
        return redirect('despesa_lista')

    return render(request, 'core/despesa/form.html', {'form': form})


@login_required
def despesa_editar(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk)
    form = DespesaForm(request.POST or None, instance=despesa)

    if form.is_valid():
        form.save()
        messages.success(request, 'Despesa atualizada com sucesso!')
        return redirect('despesa_lista')

    return render(request, 'core/despesa/form.html', {'form': form})


@login_required
def despesa_excluir(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk)

    if request.method == 'POST':
        despesa.delete()
        messages.success(request, 'Despesa excluída!')
        return redirect('despesa_lista')

    return render(request, 'core/despesa/excluir.html', {'despesa': despesa})


# =========================
# LOGIN
# =========================

class CustomLoginView(LoginView):
    template_name = 'core/registration/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('dashboard')
