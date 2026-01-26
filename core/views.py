from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum
from django.utils.timezone import now
from datetime import date

from .models import Cliente, Equipamento, OrdemServico, Receita
from .forms import ClienteForm, EquipamentoForm, OrdemServicoForm, ReceitaForm


# =========================
# CLIENTE
# =========================
def cliente_lista(request):
    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'core/cliente/lista.html', {
        'clientes': clientes,
        'titulo': 'Clientes',
        'botao_label': '+ Novo Cliente',
        'botao_url': 'cliente_novo',
    })


def cliente_novo(request):
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('cliente_lista')

    return render(request, 'core/cliente/form.html', {'form': form})


def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('cliente_lista')

    return render(request, 'core/cliente/form.html', {'form': form})


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
def equipamento_lista(request):
    equipamentos = Equipamento.objects.select_related('cliente').all()

    return render(request, 'core/equipamento/lista.html', {
        'equipamentos': equipamentos,
        'titulo': 'Equipamentos',
        'botao_label': '+ Novo Equipamento',
        'botao_url': 'equipamento_novo',
    })


def equipamento_novo(request):
    form = EquipamentoForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Equipamento cadastrado com sucesso!')
        return redirect('equipamento_lista')

    return render(request, 'core/equipamento/form.html', {'form': form})


def equipamento_editar(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    form = EquipamentoForm(request.POST or None, instance=equipamento)

    if form.is_valid():
        form.save()
        messages.success(request, 'Equipamento atualizado com sucesso!')
        return redirect('equipamento_lista')

    return render(request, 'core/equipamento/form.html', {'form': form})


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
def os_lista(request):
    ordens = OrdemServico.objects.select_related(
        'equipamento', 'tecnico'
    ).order_by('-data_abertura')

    return render(request, 'core/os/lista.html', {
        'ordens': ordens,
        'titulo': 'Ordens de Serviço',
        'botao_label': '+ Nova OS',
        'botao_url': 'os_nova',
    })


def os_nova(request):
    form = OrdemServicoForm(request.POST or None)

    if form.is_valid():
        os = form.save(commit=False)
        os.status = 'AB'
        os.save()

        messages.success(
            request,
            f'Ordem de Serviço {os.numero_os} criada com sucesso!'
        )
        return redirect('os_lista')

    return render(request, 'core/os/form.html', {'form': form})


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
def dashboard(request):
    # Clientes
    total_clientes = Cliente.objects.count()

    # Ordens de Serviço
    os_abertas = OrdemServico.objects.filter(
        status=OrdemServico.STATUS_ABERTA
    ).count()

    os_concluidas = OrdemServico.objects.filter(
        status=OrdemServico.STATUS_CONCLUIDA
    ).count()

    # Receitas do mês atual
    hoje = date.today()
    receitas_mes = Receita.objects.filter(
        data_recebimento__year=hoje.year,
        data_recebimento__month=hoje.month
    ).aggregate(total=Sum('valor'))['total'] or 0

    # Últimas OS
    ultimas_os = OrdemServico.objects.select_related(
        'equipamento',
        'equipamento__cliente'
    ).order_by('-data_abertura')[:5]

    return render(request, 'core/dashboard.html', {
        'total_clientes': total_clientes,
        'os_abertas': os_abertas,
        'os_concluidas': os_concluidas,
        'receitas_mes': receitas_mes,
        'ultimas_os': ultimas_os,
    })
# =========================
# RECEITAS
# =========================

# =========================
# RECEITAS
# =========================

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


def receita_excluir(request, pk):
    receita = get_object_or_404(Receita, pk=pk)

    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita excluída com sucesso!')
        return redirect('receita_lista')

    return render(request, 'core/receita/excluir.html', {
        'receita': receita
    })
