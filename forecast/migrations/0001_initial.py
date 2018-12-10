# Generated by Django 2.1.4 on 2018-12-10 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=200)),
                ('temp', models.FloatField(default=0.0)),
                ('pressure', models.IntegerField(default=0)),
                ('humidity', models.IntegerField(default=0)),
                ('temp_min', models.FloatField(default=0.0)),
                ('temp_max', models.FloatField(default=0.0)),
                ('wind_speed', models.IntegerField(default=0)),
                ('wind_degree', models.IntegerField(default=0)),
                ('datetime', models.IntegerField(default=0)),
                ('clouds_all', models.IntegerField(default=0)),
                ('sys_sunrise', models.IntegerField(default=0)),
                ('sys_sunset', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='place.Location')),
            ],
            options={
                'verbose_name_plural': 'weathers',
            },
        ),
    ]
