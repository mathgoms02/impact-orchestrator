from django.urls import path
from .views import (
    CustomTokenView, RegistroUsuarioView, 
    AnalisarMatchView, NotificarAgenteView, 
    VoluntarioListCreate, CriseListCreate
)

urlpatterns = [
    path('login/', CustomTokenView.as_view(), name='login'),
    path('cadastro/', RegistroUsuarioView.as_view(), name='cadastro'),
    path('voluntarios/', VoluntarioListCreate.as_view(), name='voluntarios'),
    path('crises/', CriseListCreate.as_view(), name='crises'),
    path('match/', AnalisarMatchView.as_view(), name='match'),
    path('notificar/', NotificarAgenteView.as_view(), name='notificar'),
]