# Generated by Django 2.0.7 on 2018-07-16 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Instaclone', '0007_commentmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Instaclone.UserModel'),
        ),
    ]
