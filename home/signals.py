from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VideoProgress

@receiver(post_save, sender=VideoProgress)
def update_progress(sender, instance, **kwargs):
    # Desbloqueia o módulo "Inserção" ao acessar o módulo "Equipamento"
    if instance.equipamento_watched and not instance.insercao_watched:
        instance.insercao_watched = True
        instance.save(update_fields=['insercao_watched'])
    
    # Desbloqueia o módulo "Plataforma" ao acessar o módulo "Inserção"
    if instance.insercao_watched and not instance.plataforma_watched:
        instance.plataforma_watched = True
        instance.save(update_fields=['plataforma_watched'])
