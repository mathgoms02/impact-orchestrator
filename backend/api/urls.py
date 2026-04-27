from django.urls import path
from .views import (
    CustomTokenView, RegistroUsuarioView, 
    VoluntarioListCreate, CriseListCreate,
    MatchParaOngView, MatchParaVoluntarioView,
    NotificarVoluntarioView, ConfirmarDisponibilidadeView
)

urlpatterns = [
    path('login/', CustomTokenView.as_view(), name='login'),
    path('cadastro/', RegistroUsuarioView.as_view(), name='cadastro'),
    path('voluntarios/', VoluntarioListCreate.as_view(), name='voluntarios'),
    path('crises/', CriseListCreate.as_view(), name='crises'),
    path('matches-ong/', MatchParaOngView.as_view(), name='matches-ong'),
    path('matches-voluntario/', MatchParaVoluntarioView.as_view(), name='matches-voluntario'),
    path('notificar-voluntario/', NotificarVoluntarioView.as_view(), name='notificar-voluntario'),
    path('confirmar-presenca/', ConfirmarDisponibilidadeView.as_view(), name='confirmar-presenca'),
]