from django.urls import path
from .views import (
    IndexView,
    LoginView,
    PilaresView,
    EquipamentoSelecaoView,
    InsercaoView,
    PlataformaView,
    VideoIsca2GView,
    VideoIsca4GView,
    VideoQueclinkView,
    VideoIsca419View,
    VideoInsercaoView,
    VideoPlataformaView,
    VideoPilaresView,
    mark_video_completed,
    check_progress  # Importa a função check_progress
)

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', LoginView.as_view(), name='login'),
    path('pilares/', PilaresView.as_view(), name='pilares'),
    path('equipamento-selecao/', EquipamentoSelecaoView.as_view(), name='equipamento-selecao'),
    path('insercao/', InsercaoView.as_view(), name='insercao'),
    path('plataforma/', PlataformaView.as_view(), name='plataforma'),
    path('video-isca2g/', VideoIsca2GView.as_view(), name='video-isca2g'),
    path('video-isca4g/', VideoIsca4GView.as_view(), name='video-isca4g'),
    path('video-queclink/', VideoQueclinkView.as_view(), name='video-queclink'),
    path('video-isca419/', VideoIsca419View.as_view(), name='video-isca419'),
    path('video-insercao/', VideoInsercaoView.as_view(), name='video-insercao'),
    path('video-plataforma/', VideoPlataformaView.as_view(), name='video-plataforma'),
    path('video-pilares/', VideoPilaresView.as_view(), name='video-pilares'),
    path('mark_video_completed/<str:video_type>/', mark_video_completed, name='mark_video_completed'),
    path('check-progress/', check_progress, name='check_progress'),  # Adiciona a URL para check_progress
]
