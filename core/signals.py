from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import OrdemServico, Receita


@receiver(post_save, sender=OrdemServico)
def criar_receita_ao_concluir_os(sender, instance, created, **kwargs):
    # Só cria receita quando a OS for CONCLUÍDA
    if instance.status == 'CO':

        # Evita criar receita duplicada
        if not Receita.objects.filter(ordem_servico=instance).exists():
            Receita.objects.create(
                ordem_servico=instance,
                descricao=f"Serviço - OS {instance.numero_os}",
                valor=instance.valor_servico,
                data_recebimento=timezone.now().date(),  # 🔴 AQUI ESTÁ A CORREÇÃO
                metodo_pagamento='Pendente',
                status_pagamento='Pendente'
            )
