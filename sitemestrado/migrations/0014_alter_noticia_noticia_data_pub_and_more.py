# Generated by Django 4.1.7 on 2023-05-12 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemestrado', '0013_alter_post_disciplina'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='noticia_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 12, 53, 48, 742644)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 12, 53, 48, 743642)),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='resposta_data_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 12, 53, 48, 743642)),
        ),
    ]
