# Generated by Django 5.1.2 on 2024-11-07 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_videoprogress_equipamento_time_watched_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoprogress',
            name='equipamento_time_watched',
        ),
        migrations.RemoveField(
            model_name='videoprogress',
            name='insercao_time_watched',
        ),
        migrations.RemoveField(
            model_name='videoprogress',
            name='pilar_time_watched',
        ),
        migrations.RemoveField(
            model_name='videoprogress',
            name='plataforma_time_watched',
        ),
    ]
