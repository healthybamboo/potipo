# Generated by Django 3.0.8 on 2020-11-07 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0007_question_parent_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='threads.Category'),
        ),
        migrations.AlterField(
            model_name='question',
            name='parent_category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='threads.ParentCategory'),
        ),
    ]
