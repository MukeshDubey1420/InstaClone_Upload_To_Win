# Generated by Django 2.0.7 on 2018-07-07 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Instaclone', '0006_likemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=555)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Instaclone.PostModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Instaclone.UserModel')),
            ],
        ),
    ]
