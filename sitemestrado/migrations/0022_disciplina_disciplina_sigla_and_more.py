# Generated by Django 4.1.7 on 2023-05-13 15:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemestrado', '0021_remove_evento_participantes_professores_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='disciplina_sigla',
            field=models.CharField(default='xd', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='noticia',
            name='noticia_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 13, 16, 37, 17, 119040)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 13, 16, 37, 17, 120082)),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='resposta_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 13, 16, 37, 17, 120082)),
        ),
    ]
