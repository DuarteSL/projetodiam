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
    path('noticia_<int:noticia_id>', views.detalhenoticia, name="detalhenoticia"), 
    path('adicionarevento', views.adicionarevento, name="adicionarevento"),
    path('evento_<int:evento_id>', views.detalheevento, name="detalheevento"),
    path('utilizador_<int:outrapessoa_id>', views.infooutrapessoa, name="infooutrapessoa"),
    path('editarinfopessoal', views.editarinfopessoal, name="editarinfopessoal"),
    path('criarpost', views.criarpost, name="criarpost"),
    path('searchuser',views.searchuser, name="searchuser"),
    path('searcheventos',views.searcheventos, name="searcheventos"),
    path('post_<int:post_id>', views.detalhepost, name="detalhepost"),
    path('disciplina_<int:disc_id>',views.detalhedisc, name="detalhedisc"),
    path('searchdisciplina',views.searchdisciplina,name ="searchdisciplina"),
    path('searchpost',views.searchpost,name="searchpost"),
]