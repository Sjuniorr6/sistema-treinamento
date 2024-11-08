from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, VideoProgress
import json

# View de Login personalizada para autenticação
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        empresa_input = request.POST.get('empresa')  # Empresa inserida no formulário

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verifica se o usuário possui um perfil e se a empresa coincide
            if UserProfile.objects.filter(user=user, empresa=empresa_input).exists():
                login(request, user)
                return redirect('index')  # Redireciona para a página index após login bem-sucedido
            else:
                messages.error(request, "A empresa fornecida não corresponde ao perfil.")
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
        return render(request, 'login.html')


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'
    
    perguntas_respostas = {
        1: "Como identificar a numeração da isca? : A isca terá uma etiqueta, nomeada como IMEI, nela você irá desconsiderar os 5 primeiros dígitos e o último, e irá considerar os 9 dígitos restantes. Exemplo: xxxxx-109200899-x.",
        2: "Qual a durabilidade da bateria? : A durabilidade da bateria vai depender do intervalo de transmissão do seu equipamento. Exemplo: Intervalo de 30 minutos (equipamento atualiza a cada 30 min), durabilidade de 15 dias.",
        3: "O que é GPS? : O GPS é quando a isca está comunicando via satélite, o que significa que é uma posição precisa.",
        4: "O que é LBS? : O LBS é quando o equipamento faz triangulação com as antenas localizadas na região, e ele irá gerar a posição aproximada.",
        5: "O equipamento atualiza conectado no carregador? : Não, o equipamento não posiciona enquanto conectado no carregador, pois entra em stand by.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtém ou cria o progresso do usuário para controlar o desbloqueio dos módulos
        progress, created = VideoProgress.objects.get_or_create(user=self.request.user)
        context['progress'] = progress

        # Formata as perguntas e respostas para exibição no template
        perguntas_formatadas = {
            key: {
                'pergunta': pergunta.strip(),
                'resposta': resposta.strip()
            }
            for key, value in self.perguntas_respostas.items()
            for pergunta, resposta in [value.split(':', 1)]
        }
        context['perguntas_respostas'] = perguntas_formatadas
        return context

# Marcação de vídeo concluído
@csrf_exempt
@login_required
def mark_video_completed(request, video_type):
    if request.method == 'POST':
        progress, created = VideoProgress.objects.get_or_create(user=request.user)
        data = json.loads(request.body)
        time_watched = data.get('time_watched', 0)

        # Atualiza o progresso do vídeo com base no tipo
        if video_type == "pilar":
            progress.pilar_watched = True
            progress.pilar_time_watched += time_watched
        elif video_type == "equipamento":
            progress.equipamento_watched = True
            progress.equipamento_time_watched += time_watched
        elif video_type == "insercao":
            progress.insercao_watched = True
            progress.insercao_time_watched += time_watched
        elif video_type == "plataforma":
            progress.plataforma_watched = True
            progress.plataforma_time_watched += time_watched

        progress.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})


# Views para desbloqueio automático ao serem acessadas

@method_decorator(login_required, name='dispatch')
class PilaresView(TemplateView):
    template_name = 'pilares.html'

    def get(self, request, *args, **kwargs):
        # Libera o módulo "Equipamento" ao acessar "Pilares"
        progress, created = VideoProgress.objects.get_or_create(user=request.user)
        if not progress.equipamento_watched:
            progress.equipamento_watched = True
            progress.save(update_fields=['equipamento_watched'])
            print("Equipamento liberado para o usuário:", request.user.username)  # Depuração
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class EquipamentoSelecaoView(TemplateView):
    template_name = 'equipamento-selecao.html'

    def get(self, request, *args, **kwargs):
        # Libera o módulo "Inserção" ao acessar "Equipamento"
        progress, created = VideoProgress.objects.get_or_create(user=request.user)
        if not progress.insercao_watched:
            progress.insercao_watched = True
            progress.save(update_fields=['insercao_watched'])
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class InsercaoView(TemplateView):
    template_name = 'insercao.html'

    def get(self, request, *args, **kwargs):
        # Libera o módulo "Plataforma" ao acessar "Inserção"
        progress, created = VideoProgress.objects.get_or_create(user=request.user)
        if not progress.plataforma_watched:
            progress.plataforma_watched = True
            progress.save(update_fields=['plataforma_watched'])
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PlataformaView(TemplateView):
    template_name = 'plataforma.html'


# Outras Views para Vídeos de Treinamento
@method_decorator(login_required, name='dispatch')
class VideoIsca2GView(TemplateView):
    template_name = "video-isca2g.html"


@method_decorator(login_required, name='dispatch')
class VideoIsca4GView(TemplateView):
    template_name = "video-isca4g.html"


@method_decorator(login_required, name='dispatch')
class VideoQueclinkView(TemplateView):
    template_name = "video-queclink.html"


@method_decorator(login_required, name='dispatch')
class VideoPilaresView(TemplateView):
    template_name = 'video-pilares.html'


@method_decorator(login_required, name='dispatch')
class VideoIsca419View(TemplateView):
    template_name = 'video-isca419.html'


@method_decorator(login_required, name='dispatch')
class VideoInsercaoView(TemplateView):
    template_name = 'video-insercao.html'


@method_decorator(login_required, name='dispatch')
class VideoPlataformaView(TemplateView):
    template_name = 'video-plataforma.html'



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import VideoProgress

@login_required
def check_progress(request):
    progress, created = VideoProgress.objects.get_or_create(user=request.user)
    return JsonResponse({
        'equipamento_watched': progress.equipamento_watched,
        'insercao_watched': progress.insercao_watched,
        'plataforma_watched': progress.plataforma_watched,
    })