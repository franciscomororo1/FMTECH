from django.db import models
from django.utils import timezone


# MODEL DE CLIENTE

class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=150)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=20)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail')
    endereco = models.CharField('Endereço', max_length=255)
    data_cadastro = models.DateField('Data de cadastro', auto_now_add=True)

    def __str__(self):
        return self.nome

# MODEL DE EQUIPAMENTO

class Equipamento(models.Model):
    TIPO_CHOICES = [
        ('PC', 'Computador'),
        ('NB', 'Notebook'),
        ('IMP', 'Impressora'),
        ('MON', 'Monitor'),
        ('TV', 'Televisão'),
        ('PER', 'Periférico'),
    ]
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='equipamentos'
    )
    tipo = models.CharField('Tipo', max_length=3, choices=TIPO_CHOICES)
    marca = models.CharField('Marca', max_length=100)
    modelo = models.CharField('Modelo', max_length=100)
    numero_serie = models.CharField('Número de série', max_length=100, blank=True)
    descricao = models.TextField('Descrição', blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.marca} {self.modelo}"

# MODEL DE TÉCNICO

class Tecnico(models.Model):
    nome = models.CharField('Nome', max_length=150)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail')
    ativo = models.BooleanField('Ativo', default=True)

    def __str__(self):
        return self.nome

# MODEL DE ORDEM DE SERVIÇO

class OrdemServico(models.Model):

    STATUS_ABERTA = 'AB'
    STATUS_ANDAMENTO = 'AN'
    STATUS_AGUARDANDO = 'AP'
    STATUS_CONCLUIDA = 'CO'
    STATUS_CANCELADA = 'CA'

    STATUS_CHOICES = [
        (STATUS_ABERTA, 'Aberta'),
        (STATUS_ANDAMENTO, 'Em andamento'),
        (STATUS_AGUARDANDO, 'Aguardando peça'),
        (STATUS_CONCLUIDA, 'Concluída'),
        (STATUS_CANCELADA, 'Cancelada'),
    ]


    numero_os = models.CharField(
        'Número da OS',
        max_length=20,
        unique=True,
        blank=True,
        editable=False
    )

    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name='ordens_servico'
    )

    tecnico = models.ForeignKey(
        Tecnico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordens_servico'
    )

    data_abertura = models.DateField(
        'Data de abertura',
        auto_now_add=True
    )

    data_fechamento = models.DateField(
        'Data de fechamento',
        null=True,
        blank=True
    )

    status = models.CharField(
    'Status',
    max_length=2,
    choices=STATUS_CHOICES,
    default=STATUS_ABERTA
)


    defeito_relatado = models.TextField('Defeito relatado')
    diagnostico = models.TextField('Diagnóstico', blank=True)
    solucao = models.TextField('Solução', blank=True)

    valor_servico = models.DecimalField(
        'Valor do serviço',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):
        if not self.numero_os:
            ano = timezone.now().year

            ultima_os = (
                OrdemServico.objects
                .filter(numero_os__startswith=f'OS-{ano}-')
                .order_by('-id')
                .first()
            )

            if ultima_os:
                ultimo_numero = int(ultima_os.numero_os.split('-')[-1])
                proximo_numero = ultimo_numero + 1
            else:
                proximo_numero = 1

            self.numero_os = f'OS-{ano}-{proximo_numero:04d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_os


# MODEL DE SERVIÇO

class Servico(models.Model):
    descricao = models.CharField('Descrição', max_length=150)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descricao

# MODEL DE SERVIÇO POR ORDEM DE SERVIÇO

class OrdemServicoServico(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='itens_servico'
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE
    )
    quantidade = models.PositiveIntegerField('Quantidade')

    def __str__(self):
        return f"{self.servico} ({self.quantidade})"


# MODEL FINANCEIRO (RECEITA)

class Receita(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='receitas'
    )
    descricao = models.CharField('Descrição', max_length=150)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    data_recebimento = models.DateField('Data de recebimento')
    metodo_pagamento = models.CharField('Método de pagamento', max_length=30)
    status_pagamento = models.CharField('Status do pagamento', max_length=30)

    def __str__(self):
        return self.descricao

# MODEL FINANCEIRO (DESPESAS)

class Despesa(models.Model):

    STATUS_PENDENTE = 'PE'
    STATUS_PAGA = 'PA'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_PAGA, 'Paga'),
    ]

    descricao = models.CharField('Descrição', max_length=150)

    valor = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2
    )

    data_despesa = models.DateField(
        'Data',
        default=timezone.now
    )

    status = models.CharField(
        'Status',
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE
    )

    observacao = models.TextField('Observação', blank=True)

    def __str__(self):
        return self.descricao