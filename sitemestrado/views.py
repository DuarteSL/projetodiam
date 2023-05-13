from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Aluno, Disciplina, Noticia, Evento, Post, Resposta
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
    if request.user.aluno:
        eventos_list = request.user.aluno.eventos.all()
    context = {
         'noticias_list' : noticias_list,
         'eventos_list' : eventos_list
    }
    return render(request, 'sitemestrado/infopessoal.html', context)


def editarinfopessoal(request):
    if request.method == "POST" :
        user = User.objects.get(id=request.user.id)
        if request.POST.get("primnome"):
            user.first_name= request.POST.get("primnome")
        if request.POST.get("ultnome"):
            user.last_name=request.POST.get("ultnome")
        if request.POST.get("email"):
            user.email= request.POST.get("email")
        if user.aluno:
            aluno = Aluno.objects.get(user_id=request.user.id)
            if request.POST.get("area_trab"):
                aluno.area_trab= request.POST.get("area_trab")
            if request.POST.get("linkedin"):
                aluno.linkedin = request.POST.get("linkedin")
            privado = request.POST.get('privado')
            if privado == 'on':
                aluno.is_privado = True
            else:
                aluno.is_privado = False
            if 'imagem' in request.FILES:
                imagem = request.FILES.get('imagem')
                fs = FileSystemStorage()
                imagename = fs.save(imagem.name,imagem)
                aluno.add_foto("/sitemestrado/static/media/" + imagename)
            aluno.save()
        user.save()
        return HttpResponseRedirect(reverse('sitemestrado:infopessoal'))
    return render(request, 'sitemestrado/editarinfopessoal.html')

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
        if 'ficheiros' in request.FILES:
            ficheiros = request.FILES.getlist('ficheiros')
            fs = FileSystemStorage()
            for f in ficheiros:
                ficheironame = fs.save(f.name,f)
                q.adicionar_ficheiro("/sitemestrado/static/media/" + ficheironame,ficheironame)
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
        if 'ficheiros' in request.FILES:
            ficheiros = request.FILES.getlist('ficheiros')
            fs = FileSystemStorage()
            for f in ficheiros:
                ficheironame = fs.save(f.name,f)
                q.adicionar_ficheiro("/sitemestrado/static/media/" + ficheironame,ficheironame)
        return HttpResponseRedirect(reverse('sitemestrado:index'))
    return render(request, 'sitemestrado/adicionarevento.html')

def detalheevento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    inscrito = False
    if request.user.is_authenticated:
        if not request.user.is_staff: 
            if request.user.aluno:
                inscrito = Evento.isInscrito(evento,request.user)
    if request.method == 'POST':
        if request.user.aluno:
            if evento.participantes_alunos.contains(request.user.aluno):
                evento.remove_inscrito(request.user)
            else:
                evento.add_inscrito(request.user)
        return HttpResponseRedirect(reverse('sitemestrado:detalheevento',args=[evento_id]))
    return render(request, 'sitemestrado/detalheevento.html',{'evento' : evento, 'inscrito': inscrito})

def criarpost(request):
    if request.method == 'POST':
        nome = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        referenciayoutube = request.POST.get('referenciayoutube')
        disc = request.POST.get('disciplina')
        if(disc):
            d = Disciplina.objects.get(pk=disc)
        else:
            d= None
        q = Post(post_nome=nome, 
                    post_conteudo=conteudo, 
                    referencia_youtube = referenciayoutube,
                    post_autor=request.user.first_name + " " + request.user.last_name, 
                    post_autor_id=request.user.id,
                    disciplina=d
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
        if 'ficheiros' in request.FILES:
            ficheiros = request.FILES.getlist('ficheiros')
            fs = FileSystemStorage()
            for f in ficheiros:
                ficheironame = fs.save(f.name,f)
                q.adicionar_ficheiro("/sitemestrado/static/media/" + ficheironame,ficheironame)
        return HttpResponseRedirect(reverse('sitemestrado:forum'))
    disciplinas_list = request.user.aluno.disciplinas.all()
    context = { 'disciplinas_list' : disciplinas_list}
    return render(request, 'sitemestrado/criarpost.html',context)

def searchuser(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        listauser =User.objects.filter(first_name__contains=searched) | User.objects.filter(last_name__contains=searched) 
        #| User.objects.filter(area_trab__contains=searched)
        return render(request, 'sitemestrado/searchuser.html',{'searched':searched,'listausers':listauser})  
    return render(request, 'sitemestrado/searchuser.html')      


def searcheventos(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        lista = Evento.objects.filter(evento_nome__contains=searched) | Evento.objects.filter(evento_conteudo__contains=searched)
        return render(request, 'sitemestrado/searcheventos.html',{'searched':searched,'lista_eventos':lista})  
    return render(request, 'sitemestrado/searcheventos.html')   


def detalhepost(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    if request.method == "POST":
        resposta = request.POST.get('resposta')
        q = Resposta(post=post,
                     resposta_autor = request.user.first_name + " " + request.user.last_name, 
                     resposta_autor_id = request.user.id,
                     resposta_conteudo = resposta
                     )
        q.save()
        post.add_resposta()
        return HttpResponseRedirect(reverse('sitemestrado:detalhepost',args=[post_id]))
    return render(request, 'sitemestrado/detalhepost.html',{'post' : post})

def disciplinas(request):
    disciplinas_list = Disciplina.objects.all()
    context = {
        'disciplinas_list' : disciplinas_list,
    }
    return render(request, 'sitemestrado/disciplinas.html',context)

def criardisciplina(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sigla = request.POST.get('sigla')
        disc = Disciplina(disciplina_nome=nome,disciplina_sigla=sigla)
        disc.save()
        return HttpResponseRedirect(reverse('sitemestrado:disciplinas')) 
    return render(request, 'sitemestrado/criardisciplina.html')

@login_required(login_url='/sitemestrado/loginpage')
def detalhedisc(request, disc_id):
    disciplina = get_object_or_404(Disciplina,pk=disc_id)
    post_list = Post.objects.filter(disciplina=disciplina)
    users_list = User.objects.all()
    if request.method == 'POST':
        profIDrem = request.POST.get('removerProfesor')
        profIDadd = request.POST.get('adicionarProfesor')
        if profIDrem:
            professor = Aluno.objects.get(user_id=profIDrem)
            if(professor):
                professor.disciplinas.remove(disciplina)
        if profIDadd:
            professor = Aluno.objects.get(user_id=profIDadd)
            if(professor):
                professor.disciplinas.add(disciplina)
        return HttpResponseRedirect(reverse('sitemestrado:detalhedisc',args=[disc_id]))
    return render(request, 'sitemestrado/detalhedisc.html',{'disciplina' : disciplina, 'post_list' : post_list,'users_list': users_list})

def searchdisciplina(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        lista =Disciplina.objects.filter(disciplina_nome__contains=searched)
        return render(request, 'sitemestrado/searchdisciplina.html',{'searched':searched,'lista_disciplina':lista})  
    return render(request, 'sitemestrado/searchdisciplina.html')      

    
def searchpost(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        lista = Post.objects.filter(post_nome__contains=searched) | Post.objects.filter(post_conteudo__contains=searched)
        return render(request, 'sitemestrado/searchpost.html',{'searched':searched,'lista_post':lista})  
    return render(request, 'sitemestrado/searchpost.html')  


def infooutrapessoa(request,outrapessoa_id):
    user = get_object_or_404(User, pk=outrapessoa_id)
    if request.method == "POST":
        if user.aluno.is_professor:
            user.aluno.set_aluno()
        else:
            user.aluno.set_professor()
        return HttpResponseRedirect(reverse( 'sitemestrado:infooutrapessoa',args=[user.id]))
    return render(request, 'sitemestrado/infooutrapessoa.html',{'outrapessoa' : user})
