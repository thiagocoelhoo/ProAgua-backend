# Generated by Django 4.2.1 on 2023-06-07 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Edificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, verbose_name='código')),
                ('nome', models.CharField(max_length=80, verbose_name='nome da edificação')),
                ('bloco', models.CharField(choices=[('L', 'leste'), ('O', 'oeste')], default=('L', 'leste'), max_length=1, verbose_name='bloco')),
            ],
        ),
        migrations.CreateModel(
            name='PontoColeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ambiente', models.CharField(max_length=120, verbose_name='ambiente')),
                ('tipo', models.CharField(choices=[('BE', 'Bebedouro'), ('TO', 'Torneira'), ('RS', 'Reservatório superior'), ('RI', 'Reservatório inferior')], default=('BE', 'Bebedouro'), max_length=2)),
                ('edificacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proagua.edificacao', verbose_name='edificação')),
                ('pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='proagua.pontocoleta', verbose_name='Ponto de coleta pai')),
            ],
        ),
        migrations.CreateModel(
            name='Coleta',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.FloatField(verbose_name='temperatura')),
                ('cloro_residual_livre', models.FloatField(verbose_name='cloro residual livre')),
                ('cloro_total', models.FloatField(verbose_name='cloro total')),
                ('turbidez', models.FloatField(verbose_name='turbidez')),
                ('coliformes_totais', models.BooleanField(verbose_name='coliformes totais')),
                ('escherichia', models.BooleanField(verbose_name='escherichia')),
                ('cor', models.CharField(max_length=20, verbose_name='cor')),
                ('date', models.DateTimeField(verbose_name='data da coleta')),
                ('ordem', models.CharField(choices=[('C', 'Coleta'), ('R', 'Recoleta')], default=('C', 'Coleta'), max_length=1)),
                ('amostragem', models.PositiveIntegerField(default=0, verbose_name='amostragem')),
                ('ponto_coleta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coletas', to='proagua.pontocoleta', verbose_name='ponto de coleta')),
                ('responsavel', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='responsáveis')),
            ],
        ),
    ]
