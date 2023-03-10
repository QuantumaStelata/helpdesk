# Generated by Django 4.1.6 on 2023-02-03 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vcs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_create', models.DateTimeField(auto_now_add=True)),
                ('dt_update', models.DateTimeField(auto_now=True)),
                ('version', models.UUIDField(default=uuid.uuid4)),
                ('type', models.CharField(choices=[('select', 'select'), ('radio', 'radio'), ('checkbox', 'checkbox'), ('text', 'text'), ('number', 'number'), ('date', 'date'), ('time', 'time'), ('datetime', 'datetime'), ('image', 'image'), ('file', 'file')], max_length=10)),
                ('label', models.CharField(blank=True, max_length=128)),
                ('placeholder', models.CharField(blank=True, max_length=128)),
                ('help_text', models.CharField(blank=True, max_length=128)),
                ('min_length', models.IntegerField(blank=True, null=True)),
                ('max_length', models.IntegerField(blank=True, null=True)),
                ('required', models.BooleanField(default=False)),
                ('initial', models.CharField(blank=True, max_length=128)),
                ('is_start', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='vcs.branch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_create', models.DateTimeField(auto_now_add=True)),
                ('dt_update', models.DateTimeField(auto_now=True)),
                ('version', models.UUIDField(default=uuid.uuid4)),
                ('text', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='vcs.branch')),
                ('child_fields', models.ManyToManyField(blank=True, related_name='parent_nodes', to='helpdesk.field')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('original', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='helpdesk.node')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='field',
            name='child_nodes',
            field=models.ManyToManyField(blank=True, related_name='parent_fields', to='helpdesk.node'),
        ),
        migrations.AddField(
            model_name='field',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='field',
            name='original',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='helpdesk.field'),
        ),
    ]
