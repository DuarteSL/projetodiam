# Generated by Django 4.1.7 on 2023-05-12 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemestrado', '0015_post_post_nr_respostas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='evento_nr_inscritos',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='noticia_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 18, 45, 56, 534722)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 18, 45, 56, 535738)),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='resposta_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 18, 45, 56, 535738)),
        ),
    ]
