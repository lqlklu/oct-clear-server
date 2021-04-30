# Generated by Django 3.1.7 on 2021-04-30 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oct_denoise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userauthmodel',
            name='email',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='userauthmodel',
            name='password',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='userauthmodel',
            name='uid',
            field=models.BigIntegerField(auto_created=True, default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='uid',
            field=models.BigIntegerField(auto_created=True, default=0, unique=True),
        ),
    ]
