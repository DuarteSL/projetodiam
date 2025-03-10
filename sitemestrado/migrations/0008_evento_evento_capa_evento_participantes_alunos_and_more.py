# Generated by Django 4.1.7 on 2023-05-10 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemestrado', '0007_alter_ficheiro_evento_alter_ficheiro_noticia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='evento_capa',
            field=models.TextField(default='/sitemestrado/static/media/channel-6.jpeg'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='participantes_alunos',
            field=models.ManyToManyField(default=None, related_name='participantes_alunos', to='sitemestrado.aluno'),
        ),
        migrations.AddField(
            model_name='evento',
            name='participantes_professores',
            field=models.ManyToManyField(default=None, related_name='participantes_professores', to='sitemestrado.professor'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='noticia_capa',
            field=models.TextField(default='/sitemestrado/static/media/channel-6.jpeg'),
            preserve_default=False,
        ),
    ]
