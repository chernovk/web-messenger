# Generated by Django 3.1.6 on 2021-02-05 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
                ('interlocutor_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interlocutor_1', to=settings.AUTH_USER_MODEL)),
                ('interlocutor_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interlocutor_2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
    ]
