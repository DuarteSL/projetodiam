# Generated by Django 4.1.7 on 2023-05-12 22:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemestrado', '0016_evento_evento_nr_inscritos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='imagem',
            field=models.TextField(default='\\sitemestrado\\static\\imagens\\defaultprofilepic.png'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='noticia_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 23, 41, 15, 660244)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 23, 41, 15, 661259)),
        ),
        migrations.AlterField(
            model_name='professor',
            name='imagem',
            field=models.TextField(default='\\sitemestrado\\static\\imagens\\defaultprofilepic.png'),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='resposta_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 23, 41, 15, 661259)),
        ),
    ]
