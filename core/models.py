from django.db import models


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
    STATUS_CHOICES = [
        ('AB', 'Aberta'),
        ('AN', 'Em andamento'),
        ('AP', 'Aguardando peça'),
        ('CO', 'Concluída'),
        ('CA', 'Cancelada'),
    ]

    numero_os = models.CharField('Número da OS', max_length=20, unique=True)
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name='ordens_servico'
    )
    tecnico = models.ForeignKey(
        Tecnico,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ordens_servico'
    )
    data_abertura = models.DateField('Data de abertura', auto_now_add=True)
    data_fechamento = models.DateField('Data de fechamento', null=True, blank=True)
    status = models.CharField('Status', max_length=2, choices=STATUS_CHOICES)
    defeito_relatado = models.TextField('Defeito relatado')
    diagnostico = models.TextField('Diagnóstico', blank=True)
    solucao = models.TextField('Solução', blank=True)
    valor_servico = models.DecimalField('Valor do serviço', max_digits=10, decimal_places=2)

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
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='despesas'
    )
    descricao = models.CharField('Descrição', max_length=150)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    data_pagamento = models.DateField('Data de pagamento')
    categoria = models.CharField('Categoria', max_length=50)

    def __str__(self):
        return self.descricao




