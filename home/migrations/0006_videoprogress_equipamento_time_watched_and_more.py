# Generated by Django 5.1.2 on 2024-11-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoprogress',
            name='equipamento_time_watched',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='videoprogress',
            name='insercao_time_watched',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='videoprogress',
            name='pilar_time_watched',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='videoprogress',
            name='plataforma_time_watched',
            field=models.FloatField(default=0.0),
        ),
    ]
