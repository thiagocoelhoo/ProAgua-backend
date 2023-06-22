from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home),
    
    path('pontos_coletas/', views.pontos_coletas, name='admin_pontos_coletas'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('ponto_coleta/<int:ponto_id>/', views.ponto_coleta, name='admin_ponto_coleta'),
    path('ponto_coleta/<int:ponto_id>/<int:amostragem>/', views.ponto_coleta_relatorio, name='admin_ponto_coleta_amostragem'),
    path('criar_ponto/', views.criar_ponto, name='criar_ponto'),
    
    path('criar_coleta/', views.criar_coleta, name='criar_coleta'),
    path('editar_coleta/<int:coleta_id>/', views.editar_coleta, name='editar_coleta'),
    
    path('configuracoes/', views.configuracoes, name='admin_configuracoes'),
    
    path('edificacoes/', views.edificacoes, name='admin_edificacoes'),
    path('edificacao/<int:edificacao_id>/', views.edificacao, name='editar_edificacao'),
    path('criar_edificacao/', views.criar_edificacao, name='criar_edificacao'),

    path('accounts/', include('django.contrib.auth.urls')),
]
