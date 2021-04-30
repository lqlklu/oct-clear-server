# Generated by Django 3.1.7 on 2021-04-30 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='filename', max_length=256)),
                ('file', models.FileField(upload_to='.')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.BigIntegerField(default=0)),
                ('path', models.CharField(default='', max_length=256)),
                ('disable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserAuthModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.BigIntegerField(auto_created=True, default=0)),
                ('email', models.CharField(default='', max_length=256)),
                ('password', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.BigIntegerField(auto_created=True, default=0)),
                ('email', models.CharField(default='', max_length=256)),
            ],
        ),
    ]
