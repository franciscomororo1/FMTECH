from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Equipamento, OrdemServico
from .forms import ClienteForm, EquipamentoForm, OrdemServicoForm
from django.contrib import messages
from django.urls import reverse



# =========================
# CLIENTE
# =========================
def cliente_lista(request):
    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'core/cliente/lista.html', {
        'clientes': clientes,
        'titulo': 'Clientes',
        'botao_label': '+ Novo Cliente',
        'botao_url': reverse('cliente_novo'),
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

    context = {
        'equipamentos': equipamentos,
        'titulo': 'Equipamentos',
        'botao_url': '/equipamentos/novo/',
        'botao_label': '+ Novo Equipamento',
    }

    return render(request, 'core/equipamento/lista.html', context)

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
        'botao_url': reverse('os_nova'),
    })


def os_nova(request):
    form = OrdemServicoForm(request.POST or None)

    if form.is_valid():
        os = form.save(commit=False)
        os.status = 'AB'
        os.save()

        messages.success(request, f'Ordem de Serviço {os.numero_os} criada com sucesso!')
        return redirect('os_lista')

    return render(request, 'core/os/form.html', {'form': form})


def os_editar(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)
    form = OrdemServicoForm(request.POST or None, instance=os)

    if form.is_valid():
        form.save()
        messages.success(request, f'Ordem de Serviço {os.numero_os} atualizada!')
        return redirect('os_lista')

    return render(request, 'core/os/form.html', {'form': form, 'os': os})


def os_excluir(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':
        numero = os.numero_os
        os.delete()
        messages.success(request, f'Ordem de Serviço {numero} excluída!')
        return redirect('os_lista')

    return render(request, 'core/os/excluir.html', {'os': os})
