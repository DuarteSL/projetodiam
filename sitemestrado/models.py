from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Aluno(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    imagem = models.TextField()
    is_public = models.BooleanField(default=True)

    ''' precisa de mais campos para a pagina de info pessoal'''

    def __str__(self):
        return self.user.username
    

class Professor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    imagem = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    

class Evento(models.Model):
    evento_nome = models.CharField(max_length=200)
    evento_conteudo = models.TextField()
    evento_data = models.DateTimeField() 
    evento_capa = models.TextField()
    evento_autor = models.CharField(max_length=200)
    evento_autor_id = models.IntegerField()

    participantes_alunos = models.ManyToManyField('Aluno',related_name='participantes_alunos', default = None)
    participantes_professores = models.ManyToManyField('Professor',related_name='participantes_professores', default = None)

    def __str__(self):
      return self.evento_nome
    
    def add_capa(self,capa):
       self.evento_capa=capa
       self.save()
    
    def get_next_three(lista):
       filtered = filter(lambda evento: evento.evento_data >= timezone.now(), lista)
       return list(filtered)[-3:]

   
class Noticia(models.Model):
    noticia_nome = models.CharField(max_length=200)
    noticia_conteudo = models.TextField()
    noticia_data_pub = models.DateTimeField(default=timezone.now)
    noticia_autor = models.CharField(max_length=200)
    noticia_autor_id = models.IntegerField()
    noticia_privacidade = models.BooleanField(default=False)
    noticia_capa = models.TextField()

    def __str__(self):
      return self.noticia_nome
    
    def add_capa(self,capa):
       self.noticia_capa=capa
       self.save()
    
    def adicionar_imagem(self,imagem):
       nova_imagem = Imagem(noticia=self,imagem=imagem)
       nova_imagem.save()

    def adicionar_ficheiro(self,ficheiro):
       novo_ficheiro = Ficheiro(noticia=self,ficheiro=ficheiro)
       novo_ficheiro.save()

class Disciplina(models.Model):
    disciplina_nome = models.CharField(max_length=200)
    professores = models.ManyToManyField('Professor',related_name='disciplinas', default = None)

    def __str__(self):
      return self.disciplina_nome



class Post(models.Model):
    post_nome = models.CharField(max_length=200)
    post_conteudo = models.TextField()
    post_autor = models.CharField(max_length=200)
    post_autor_id = models.IntegerField()
    post_data_pub = models.DateTimeField(default=timezone.now)
    referencia_youtube = models.TextField()

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, default = None)

    def __str__(self):
      return self.post_nome
    

class Resposta(models.Model):
   post = models.ForeignKey(Post,on_delete=models.CASCADE)
   resposta_autor = models.CharField(max_length=200)
   resposta_autor_id = models.IntegerField()
   resposta_conteudo = models.TextField()
   resposta_data_pub = models.DateTimeField(default=timezone.now)

   def __str__(self):
      return self.resposta_conteudo
   

class Ficheiro(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='ficheiros',default=None,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ficheiros',default=None,null=True)
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE, related_name='ficheiros',default=None,null=True)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='ficheiros',default=None,null=True)
    ficheiro = models.TextField()

class Imagem(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='imagens',default=None,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='imagens',default=None,null=True)
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE, related_name='imagens',default=None,null=True)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='imagens',default=None,null=True)
    imagem = models.TextField()

