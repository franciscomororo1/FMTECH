from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User, Group

from .models import OrdemServico, Receita, Profile


@receiver(pre_save, sender=OrdemServico, dispatch_uid='ordem_servico_status_change')
def detectar_mudanca_status(sender, instance, **kwargs):
    """
    Armazena o status anterior da OS para comparação no post_save
    """
    if instance.pk:
        try:
            instance._status_anterior = (
                OrdemServico.objects
                .values_list('status', flat=True)
                .get(pk=instance.pk)
            )
        except OrdemServico.DoesNotExist:
            instance._status_anterior = None
    else:
        instance._status_anterior = None


@receiver(post_save, sender=OrdemServico, dispatch_uid='criar_receita_ao_concluir_os')
def criar_receita_ao_concluir_os(sender, instance, created, **kwargs):
    """
    Cria automaticamente uma receita quando a OS for concluída
    (somente na transição de status)
    """
    status_anterior = getattr(instance, '_status_anterior', None)

    # Só executa quando o status muda para CONCLUÍDA
    if instance.status == OrdemServico.STATUS_CONCLUIDA and status_anterior != OrdemServico.STATUS_CONCLUIDA:

        Receita.objects.create(
            ordem_servico=instance,
            descricao=f'Serviço - OS {instance.numero_os}',
            valor=instance.valor_servico,
            data_recebimento=timezone.now().date(),
            metodo_pagamento='Pendente',
            status_pagamento='Pendente'
        )

@receiver(post_save, sender=User)
def criar_profile_usuario(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)