# Generated by Django 3.0.8 on 2020-10-24 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='parent_quesion',
            new_name='parent_question',
        ),
    ]
