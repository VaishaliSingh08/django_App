# Generated by Django 3.2.3 on 2021-05-21 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dummy', '0004_delete_dummyregister'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyEmailLinkcounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_count', models.IntegerField()),
            ],
            options={
                'db_table': 'verify_email_linkcounter',
                'managed': False,
            },
        ),
    ]
