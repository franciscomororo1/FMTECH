from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Equipamento, OrdemServico
from .forms import ClienteForm, EquipamentoForm, OrdemServicoForm
from datetime import date


#VIEWS DE CLIENTE

def cliente_lista(request):
    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'core/cliente/lista.html', {'clientes': clientes})


def cliente_novo(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_lista')
    else:
        form = ClienteForm()
    return render(request, 'core/cliente/form.html', {'form': form})


def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_lista')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/cliente/form.html', {'form': form})


def cliente_excluir(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_lista')
    return render(request, 'core/cliente/excluir.html', {'cliente': cliente})

# VIEWS DE EQUIPAMENTO

def equipamento_lista(request):
    equipamentos = Equipamento.objects.select_related('cliente').all()
    return render(request, 'core/equipamento/lista.html', {'equipamentos': equipamentos})


def equipamento_novo(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipamento_lista')
    else:
        form = EquipamentoForm()
    return render(request, 'core/equipamento/form.html', {'form': form})


def equipamento_editar(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            return redirect('equipamento_lista')
    else:
        form = EquipamentoForm(instance=equipamento)
    return render(request, 'core/equipamento/form.html', {'form': form})


def equipamento_excluir(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        equipamento.delete()
        return redirect('equipamento_lista')
    return render(request, 'core/equipamento/excluir.html', {'equipamento': equipamento})


# VIEWS DE ORDEM DE SERVIÇO

def os_lista(request):
    ordens = OrdemServico.objects.select_related(
        'equipamento', 'tecnico'
    ).order_by('-data_abertura')

    return render(request, 'core/os/lista.html', {'ordens': ordens})


def os_nova(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            os = form.save(commit=False)
            os.status = 'AB'
            os.save()
            return redirect('os_lista')
    else:
        form = OrdemServicoForm()

    return render(request, 'core/os/form.html', {'form': form})


def os_editar(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, instance=os)
        if form.is_valid():
            form.save()
            return redirect('os_lista')
    else:
        form = OrdemServicoForm(instance=os)

    return render(request, 'core/os/form.html', {'form': form, 'os': os})


def os_excluir(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':
        os.delete()
        return redirect('os_lista')

    return render(request, 'core/os/excluir.html', {'os': os})
