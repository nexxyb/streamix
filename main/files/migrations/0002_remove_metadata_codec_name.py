# Generated by Django 4.0.7 on 2023-12-16 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metadata',
            name='codec_name',
        ),
    ]