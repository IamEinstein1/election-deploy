# Generated by Django 3.1.1 on 2020-09-19 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_animal'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=2048)),
                ('spl_done', models.BooleanField(default=False)),
                ('aspl_done', models.BooleanField(default=False)),
                ('last_seen', models.DateTimeField()),
            ],
        ),
    ]
