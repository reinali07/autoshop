# Generated by Django 3.0.2 on 2020-09-06 01:14

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preferences', '0002_auto_20181220_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPreference',
            fields=[
                ('preferences_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='preferences.Preferences')),
                ('labour_markup', models.FloatField(default=1.0)),
                ('labour_rate', models.FloatField(default=1.0)),
            ],
            bases=('preferences.preferences',),
            managers=[
                ('singleton', django.db.models.manager.Manager()),
            ],
        ),
    ]
