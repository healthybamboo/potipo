# Generated by Django 3.0.8 on 2020-10-24 00:48

from django.db import migrations, models
import django.db.models.deletion
import threads.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('vote', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('reply_dead_line', models.DateTimeField(default=threads.models.Question.in_three_days)),
                ('all_answer_numbers', models.PositiveIntegerField(default=0)),
                ('let_answer_add', models.BooleanField(default=False)),
                ('let_reason_add', models.BooleanField(default=False)),
                ('original_question', models.PositiveIntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('question_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('vote', models.PositiveIntegerField(default=0)),
                ('parente_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reason', to='threads.Answer')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='parent_quesion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='threads.Question'),
        ),
    ]
