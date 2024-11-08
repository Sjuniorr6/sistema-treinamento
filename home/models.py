from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='midia/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} - {self.empresa}'

class VideoProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pilar_time_watched = models.FloatField(default=0.0)
    equipamento_time_watched = models.FloatField(default=0.0)
    insercao_time_watched = models.FloatField(default=0.0)
    plataforma_time_watched = models.FloatField(default=0.0)
    pilar_watched = models.BooleanField(default=False)
    equipamento_watched = models.BooleanField(default=False)  # Liberar inserção ao assistir qualquer equipamento
    insercao_watched = models.BooleanField(default=False)
    plataforma_watched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Progress"

# View para marcar o vídeo como assistido
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def mark_video_completed(request, video_type):
    if request.method == 'POST':
        print(f'Requisição recebida para marcar vídeo como assistido: {video_type}')
        progress, created = VideoProgress.objects.get_or_create(user=request.user)

        # Atualiza o progresso com base no tipo de vídeo
        if video_type == "pilar":
            progress.pilar_watched = True
        elif video_type == "equipamento":
            progress.equipamento_watched = True
        elif video_type == "insercao":
            progress.insercao_watched = True
        elif video_type == "plataforma":
            progress.plataforma_watched = True
        
        progress.save()
        print(f'Progresso atualizado: {progress.__dict__}')  # Mostra os campos do progresso
        return JsonResponse({"status": "success"})

# Sinal para criar o VideoProgress automaticamente ao criar um novo User
@receiver(post_save, sender=User)
def create_video_progress(sender, instance, created, **kwargs):
    if created:
        VideoProgress.objects.get_or_create(user=instance)

# Sinal para salvar o progresso de vídeo sempre que o User for salvo
@receiver(post_save, sender=User)
def save_video_progress(sender, instance, **kwargs):
    if hasattr(instance, 'videoprogress'):
        instance.videoprogress.save()



from django.db import models
from django.contrib.auth.models import User

class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pilar_watched = models.BooleanField(default=False)
    equipamento_watched = models.BooleanField(default=False)
    insercao_watched = models.BooleanField(default=False)
    plataforma_watched = models.BooleanField(default=False)
