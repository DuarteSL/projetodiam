from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Aluno, Noticia, Evento, Post
from datetime import datetime
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    noticias_list = Noticia.objects.order_by('-noticia_data_pub')
    eventos_list = Evento.objects.order_by('-evento_data')
    three_eventos = Evento.get_next_three(eventos_list)
    users_list = User.objects.all()
    context = {
        'noticias_list' : noticias_list,
        'three_eventos' : three_eventos,
        'users_list' : users_list 
    }
    return render(request, 'sitemestrado/index.html',context)

def infopessoal(request):
    noticias_list = Noticia.objects.order_by('-noticia_data_pub')
    eventos_list = Evento.objects.filter(evento_autor_id=request.user.id).order_by('evento_data')
    context = {
         'noticias_list' : noticias_list,
         'eventos_list' : eventos_list
    }
    return render(request, 'sitemestrado/infopessoal.html', context)

def loginpage(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('sitemestrado:index'))
        else:
            '''para depois'''
    return render(request, 'sitemestrado/loginpage.html')

def logoutpage(request):
    logout(request)
    return HttpResponseRedirect(reverse('sitemestrado:index'))

def registar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nome = request.POST.get('nome')
        apelido = request.POST.get('apelido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        privado = request.POST.get('perfilprivado')
        if privado == 'on':
            privado = True
        else:
            privado = False
        u = User.objects.create_user(username, email, password, first_name = nome, last_name= apelido)
        u.save()
        aluno = Aluno(user=u, is_privado=privado)
        aluno.save()
        return HttpResponseRedirect(reverse('sitemestrado:loginpage'))
    return render(request, 'sitemestrado/registar.html')

def eventos(request):
    eventos_list = Evento.objects.order_by('-evento_data')
    context = {
        'eventos_list' : eventos_list 
    }
    return render(request, 'sitemestrado/eventos.html',context)



def disciplinas(request):
    return render(request, 'sitemestrado/disciplinas.html')

@login_required(login_url='/sitemestrado/loginpage')
def forum(request):
    post_list = Post.objects.order_by('-post_data_pub')
    context = {
        'post_list' : post_list
    }
    return render(request, 'sitemestrado/forum.html',context)

@login_required(login_url='/sitemestrado/loginpage')
def criarnoticia(request):
    if request.method == 'POST':
        nome = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        priv = request.POST.get('privada')
        if priv == 'on':
            priv = True
        else:
            priv = False
        q = Noticia(noticia_nome=nome, 
                    noticia_conteudo=conteudo, 
                    noticia_autor=request.user.first_name + " " + request.user.last_name, 
                    noticia_autor_id=request.user.id,
                    noticia_privacidade=priv,
                    )
        if 'imagem' in request.FILES:
            imagem = request.FILES.get('imagem')
            fs = FileSystemStorage()
            imagename = fs.save(imagem.name,imagem)
            q.add_capa("/sitemestrado/static/media/" + imagename)
        q.save()
        if 'imagens' in request.FILES:
            imagens = request.FILES.getlist('imagens')
            fs = FileSystemStorage()
            for f in imagens:
                imagename = fs.save(f.name,f)
                q.adicionar_imagem("/sitemestrado/static/media/" + imagename)
        '''
        if 'ficheiros' in request.FILES:
            ficheiros = request.FILES.getlist('ficheiros')
            fs = FileSystemStorage()
            for f in ficheiros:
                ficheironame = fs.save(f,f.name)
                q.adicionar_ficheiro("/sitemestrado/static/media/" + ficheironame)
        '''
        return HttpResponseRedirect(reverse('sitemestrado:index'))
    return render(request, 'sitemestrado/criarnoticia.html')

def detalhenoticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    return render(request, 'sitemestrado/detalhenoticia.html',{'noticia' : noticia})

@login_required(login_url='/sitemestrado/loginpage')
def adicionarevento(request):
    if request.method == 'POST':
        nome = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        data = request.POST.get('data')
        q = Evento(evento_nome=nome, 
                    evento_conteudo=conteudo, 
                    evento_data=data,
                    evento_autor=request.user.first_name + " " + request.user.last_name, 
                    evento_autor_id=request.user.id,
                    )
        if 'imagem' in request.FILES:
            imagem = request.FILES.get('imagem')
            fs = FileSystemStorage()
            imagename = fs.save(imagem.name,imagem)
            q.add_capa("/sitemestrado/static/media/" + imagename)
        q.save()
        if 'imagens' in request.FILES:
            imagens = request.FILES.getlist('imagens')
            fs = FileSystemStorage()
            for f in imagens:
                imagename = fs.save(f.name,f)
                q.adicionar_imagem("/sitemestrado/static/media/" + imagename)
        '''
        if 'ficheiros' in request.FILES:
            ficheiros = request.FILES.getlist('ficheiros')
            fs = FileSystemStorage()
            for f in ficheiros:
                ficheironame = fs.save(f,f.name)
                q.adicionar_ficheiro("/sitemestrado/static/media/" + ficheironame)
        '''
        return HttpResponseRedirect(reverse('sitemestrado:index'))
    return render(request, 'sitemestrado/adicionarevento.html')

def detalheevento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    return render(request, 'sitemestrado/detalheevento.html',{'evento' : evento})

def infooutrapessoa(request,outrapessoa_id):
    outrapessoa = get_object_or_404(User, pk=outrapessoa_id)
    return render(request, 'sitemestrado/infooutrapessoa.html',{'outrapessoa' : outrapessoa})

def editarinfopessoal(request):
    return render(request, 'sitemestrado/editarinfopessoal.html')

def criarpost(request):
    if request.method == 'POST':
        nome = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        referenciayoutube = request.POST.get('referenciayoutube')
        q = Post(post_nome=nome, 
                    post_conteudo=conteudo, 
                    referencia_youtube = referenciayoutube,
                    post_autor=request.user.first_name + " " + request.user.last_name, 
                    post_autor_id=request.user.id,
                    )
        if 'imagem' in request.FILES:
            imagem = request.FILES.get('imagem')
            fs = FileSystemStorage()
            imagename = fs.save(imagem.name,imagem)
            q.add_capa("/sitemestrado/static/media/" + imagename)
        q.save()
        if 'imagens' in request.FILES:
            imagens = request.FILES.getlist('imagens')
            fs = FileSystemStorage()
            for f in imagens:
                imagename = fs.save(f.name,f)
                q.adicionar_imagem("/sitemestrado/static/media/" + imagename)
        '''
        if 'ficheiros' in request.FILES:
            ficheiros = request.FILES.getlist('ficheiros')
            fs = FileSystemStorage()
            for f in ficheiros:
                ficheironame = fs.save(f,f.name)
                q.adicionar_ficheiro("/sitemestrado/static/media/" + ficheironame)
        '''
        return HttpResponseRedirect(reverse('sitemestrado:index'))
    return render(request, 'sitemestrado/criarpost.html')

def searchuser(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        lista =User.objects.filter(first_name__contains=searched)|User.objects.filter(last_name__contains=searched)
        return render(request, 'sitemestrado/searchuser.html',{'searched':searched,'listausers':lista})  
    else:
            return render(request, 'sitemestrado/searchuser.html',{'searched':'nao funciona'})      