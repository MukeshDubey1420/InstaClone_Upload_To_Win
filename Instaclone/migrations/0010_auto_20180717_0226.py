# Generated by Django 2.0.7 on 2018-07-16 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Instaclone', '0009_categorymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Instaclone.UserModel'),
        ),
    ]
