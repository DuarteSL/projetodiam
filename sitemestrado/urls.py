from django.urls import include, path
from . import views

app_name = 'sitemestrado'

urlpatterns = [
    path("", views.index, name='index'),
    path('loginpage', views.loginpage, name="loginpage"),
    path('logoutpage', views.logoutpage, name="logoutpage"),
    path('registar', views.registar, name='registar'),
    path('eventos', views.eventos, name='eventos'),
    path('disciplinas', views.disciplinas, name="disciplinas"),
    path('forum', views.forum, name="forum"),
    path('infopessoal', views.infopessoal, name="infopessoal"),
    path('criarnoticia', views.criarnoticia, name="criarnoticia"),
    path('noticia/<int:noticia_id>', views.detalhenoticia, name="detalhenoticia"), 
    path('adicionarevento', views.adicionarevento, name="adicionarevento"),
    path('evento/<int:evento_id>', views.detalheevento, name="detalheevento"),
]