from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Noticia

# Create your views here.

def index(request):
    noticias_list = Noticia.objects.order_by('-noticia_data_pub')
    context = {
        'noticias_list' : noticias_list
    }
    return render(request, 'sitemestrado/index.html',context)


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
    return HttpResponseRedirect(reverse('votacao:index'))

def registar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        u = User.objects.create_user(username, email, password)
        u.save()
        return HttpResponseRedirect(reverse('sitemestrado:loginpage'))
    return render(request, 'sitemestrado/registar.html')

def eventos(request):
    return render(request, 'sitemestrado/eventos.html')

def infopessoal(request):
    return render(request, 'sitemestrado/infopessoal.html')

def disciplinas(request):
    return render(request, 'sitemestrado/disciplinas.html')

@login_required(login_url='/sitemestrado/loginpage')
def forum(request):
    return render(request, 'sitemestrado/forum.html')