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
]