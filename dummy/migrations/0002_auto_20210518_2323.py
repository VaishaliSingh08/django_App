# Generated by Django 3.2.3 on 2021-05-18 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dummy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('user_email', models.CharField(max_length=200)),
                ('user_contact', models.CharField(max_length=200)),
                ('user_qualification', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('re_pass', models.CharField(max_length=200)),
                ('picture', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='users',
        ),
    ]
